'''Process sunrise/sunset data from US Naval Observatory for use in NuPIC.
   
   Produces a data table with one row for each hour w/ DATETIME timestamp and
   binary value for 'dark' or 'light' at that hour, along with daylight seconds
   (calculated here), sunrise, and sunset.

   Raw data is a bit funky: 9 header rows (containing location, year, and timezone, etc.)  
   Column-wise 'duplets' are provided for each month.  First duplet element is sunrise, 
   second is sunset. Rows are days.  
   
   NB: as a practical matter, these data come with arbitrary \n characters in the header so
   ad-hoc adjustments to the data files may be needed.

   
   Specify input and output files in if __name__=='__main__' block
'''

from __future__ import print_function
import  datetime, sys, os, csv

#edit fields to skip at will but do not exclude DATE or HRMN (needed for timestamp)

###TODO: pass db, table names in as args
HEADER_ROWS=8
TABLE_NAME='sun'
DB_NAME='astro'
DEFAULT_VAL=''

#fields for the data table (keep these in the same order as established in prep_output)
fields = [{'fid':'time', 'dtype':"DATETIME" },
          {'fid':'is_daylight', 'dtype':"TINYINT" },
          {'fid':'rise', 'dtype':"DATETIME" },
          {'fid':'sset', 'dtype':"DATETIME" },
          {'fid':'seconds_daylite', 'dtype':"INT(6)" },
          {'fid':'seconds_since_rise', 'dtype':"INT(6)" },
          {'fid':'city', 'dtype':"VARCHAR(30)" },
          {'fid':'state', 'dtype':"VARCHAR(30)" },
          ]

class ParserError(Exception):
    pass

def prep_output(d):
    """ Determine: is it dark or light? Input dict has days as keys and (sunrise, sunset) as vals
        Returns a list of tuples.  Each tuple is a DATETIME object.  Contents: today, sunrise,    
        sunset, length of day"""
    out=[]
    keys=list(d.keys())
    keys.sort()
    for ts in keys: 
        #each day, starting in Jan., grab sunrise/sunset times
        srise=d[ts][0]
        sset =d[ts][1]        
        seconds_daylite=int((sset-srise).total_seconds())
        for h in range(24): #hours
            #the key is 'today'
            now = ts + datetime.timedelta(hours=h)
            
            is_daylight = int(now >= srise and now < sset)  #daylight
            if is_daylight:
                seconds_since_rise=int((now - srise).total_seconds())
            else:
                seconds_since_rise = 0
            
            #this is pretty redundant, but we'll keep our data intact at this point
            out.append((now, is_daylight, srise, sset, 
                        seconds_daylite, seconds_since_rise,
                        CITY, STATE))
    return out

def read_data(fn):  
    """reads astronomical data from Naval Observatory dump; returns
       a dict of {dates, (sunrise and sunset)}, all DATETIME objects
    """
                
    with open(fn, 'r') as infile: 
        raw=infile.readlines()
        
        #dig out the year - if type-castable to an int > 2000, call it good
        year = 0
        date_line=1
        print (raw[date_line])
        for text in raw[date_line].split():
            try:
                if int(text) > 2000:
                    year=int(text)
            except:
                pass #OK to fail silently here; we only care about the year
        if not year:
            ###todo  reload sun data here, then reload database.  seconds field was too short first time.
            raise ParserError('No valid year found.')
        
        #make sure the 'months' row is where we expect it - if not, data format changed
        month_row = date_line+5
        if not 'Jan' in raw[month_row].split()[0]:
            msg='Expecting months in row {} of {} but found {}:'
            raise ParserError(msg.format(month_row, fn, raw[6]))
        
        #dump the rest of the header - we don't need it
        raw=raw[HEADER_ROWS+1:]
        if raw[0][:2]!='01':  #should be 01 (first of jan)
            msg='header row count wrong - first line is {}'.format(raw[0])
            raise ParserError(msg)
           
        d={} #we'll store times in this dict
        
        #this just steps through each row grabbing the raw data
        for r in raw:
            if r.strip():  #controls for blank lines (or just \n)
                if 'daylight' in r:  #any alpha signals end of file
                    break
                day=int(r[0:2]   )
                cptr=4
                for m in range(1,13):
                    #check for non-empty sunrise field (none for Feb 31)
                    if r[cptr:cptr+2].strip():
                        rise_hr=int(r[cptr:cptr+2])
                        rise_min=int(r[cptr+2: cptr+5])
                        set_hr=int(r[cptr+5: cptr+7])
                        set_min=int(r[cptr+7: cptr+9])
                        
                        today = datetime.datetime(year,m,day)
                        sunrise = datetime.datetime(year, m, day, rise_hr, rise_min)
                        sunset = datetime.datetime(year, m, day, set_hr, set_min)                    
                        d[today]=(sunrise, sunset)
                        
                    cptr+=11
                
        #quick reality check on the data        
        if not (len(d)==365 or len(d)==366):
            raise ParserError("Expecting 365 or 366 days, got {}.".format(len(d)))
                    
        return d


def csv_writer(o_file):
    return csv.writer(o_file, quoting=csv.QUOTE_NONNUMERIC).writerow

def sql_writer(o_file, db=DB_NAME, table=TABLE_NAME,  new=False):
    return SqlWrite(o_file,db=DB_NAME, table=TABLE_NAME,  new=False).write
                
class SqlWrite():
    def __init__(self, o_file, db=DB_NAME, table=TABLE_NAME,  new=False):
        self.db=db
        self.table=table
        self.o_file = o_file
        ###TODO:  put # in front of these statements to prevent accidents
        
        if new:
            self.o_file.write('CREATE DATABASE IF NOT EXISTS {};\n'.format(DB_NAME))
            self.o_file.write('USE {};\n'.format(db))
            self.o_file.write("DROP TABLE IF EXISTS {};\n".format(self.table))
            s= "CREATE TABLE {} ( \n".format(table)
            for r in fields:
                s += "{} {},\n".format(r['fid'], r['dtype'])
            #trim the trailing ',' to avoid a syntax error
            s=s[:-2]
            s += ');\n'
            self.o_file.write(s)
            
    def write(self, data):
        """Writes INSERT statements for each day of the year.  Input comes in the form of a list;
           (now, is_daylight, srise, sset, day_length)"""
        
        s='INSERT INTO {} ('.format(self.table)
        cols=[]
        vals=[]

        for i, f in enumerate(fields):
            field_name = f['fid']
            cols.append(field_name)
            vals.append(data[i])
        
        s += ", ".join(i for i in cols) + ') VALUES ('
        s += ", ".join("'" + str(i) + "'" for i in vals) + ');\n'
        s=s.replace("'" + DEFAULT_VAL + "'",'NULL')
        self.o_file.write(s)

def main(fn='test.txt', o_file='sun.sql', outmode='sql', new=False):
    timestamps=read_data(fn)
    data=prep_output(timestamps)   

    with open(outfile, 'w') as o_file:        
        if outmode == 'sql':
            writer=sql_writer(o_file, new=new)
        elif outmode == 'csv':
            writer=csv_writer(o_file)        
        for d in data:
            writer(d)

if __name__=='__main__':
    #where are we?
    CITY="Austin"
    STATE="TX"   
    YEAR='2015'
    I_DIR='d://pecan//austin_sunrise' #input dir
    O_DIR='d://pecan//austin_sunrise' #output dir
    tz = -6          #US Central timezone
    
    #file specs
    fn =    '{}_{}.txt'.format(I_DIR, YEAR)       #input file
    outfile='{}_{}.sql'.format(O_DIR, YEAR)        #output file
    outmode='sql'                           #options: 'csv', 'con', 'sql'
    new=False

    #read data. add binary "is light outside" data, write data   
    main(fn, outfile, outmode, new)

    print('Done! Wrote file: {}'.format(outfile))
    
                

        
        
    