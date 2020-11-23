import os

blog_1_url = "http://www.stockfries.com/blog/1_gambling"
blog_2_url = "http://www.stockfries.com/blog/2_basics"


change_threshold = 50000

ownership_colors = [
    'rgba(0,0,255,'+str(i/100)+')' for i in range(2, 42, 2)[::-1]]
positives_colors = [
    'rgba(0,255,0,'+str(i/100)+')' for i in range(2, 42, 2)[::-1]]
negatives_colors = [
    'rgba(255,0,0,'+str(i/100)+')' for i in range(2, 42, 2)[::-1]]

figi_api_key = '34dada0c-5a22-4f5a-a095-739afe8fe591' 

scrapped_json_fn = 'json_df.txt'
scrapped_json_fn_no_ticker = 'json_df_no_ticker.txt'
scrapped_json_fn_hedgefund = 'json_df_dataByHedgeFund.txt'

fund_dict = {'Mangrove Partners': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1535392&owner=exclude&count=40&hidefilings=0',
             'Segantii': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1544676&owner=exclude&count=40&hidefilings=0',
             'MIG Capital': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1425649&owner=exclude&count=40&hidefilings=0',
             'Parametrica Asset Management Ltd': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1535090&owner=exclude&count=40&hidefilings=0',
             'Masters Capital Management': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1104186&owner=exclude&count=40&hidefilings=0',
             'Harvest Capital Strategies': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1226355&owner=exclude&count=40&hidefilings=0',
             'Anson Funds': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1491072&owner=exclude&count=40&hidefilings=0',
             'Capital Fund Management': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1323645&owner=exclude&count=40&hidefilings=0',
             'Hawk Ridge Capital Management': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1609074&owner=exclude&count=40&hidefilings=0',
             'Contrarian Capital Management': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1050417&owner=exclude&count=40&hidefilings=0',
             'Dorsal Capital Management': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1547007&owner=exclude&count=40&hidefilings=0',
             'Tide Point': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1590569&owner=exclude&count=40&hidefilings=0',
             'VR Advisory Services': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1348145&owner=exclude&count=40&hidefilings=0',
             'Long Pond Capital, LP': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1499066&owner=exclude&count=40&hidefilings=0',
             'BloombergSen U.S. Fund LP': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1641744&owner=exclude&count=40&hidefilings=0',
             'Polar Asset Management Partners': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1326389&owner=exclude&count=40&hidefilings=0',
             'PARAMETRICA ASSET MANAGEMENT LTD': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1535090&owner=exclude&count=40&hidefilings=0',
             'ABRAMS CAPITAL MANAGEMENT, L.P.': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1358706&owner=exclude&count=40&hidefilings=0',
             'AKRE CAPITAL MANAGEMENT': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1112520&owner=exclude&count=40&hidefilings=0',
             'APPALOOSA LP': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1656456&owner=exclude&count=40&hidefilings=0',
             'ARLINGTON VALUE CAPITAL, LLC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1568820&owner=exclude&count=40&hidefilings=0',
             'ATLANTIC INVESTMENT MANAGEMENT, INC.': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1063296&owner=exclude&count=40&hidefilings=0',
             'BAKER BROS. ADVISORS LP': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1263508&owner=exclude&count=40&hidefilings=0',
             'COATUE MANAGEMENT LLC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1135730&owner=exclude&count=40&hidefilings=0',
             'CORVEX MANAGEMENT LP': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1535472&owner=exclude&count=40&hidefilings=0',
             'DALAL STREET, LLC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1549575&owner=exclude&count=40&hidefilings=0',
             'ELLIOTT MANAGEMENT CORP': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1048445&owner=exclude&count=40&hidefilings=0',
             'EMINENCE CAPITAL, LP': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1107310&owner=exclude&count=40&hidefilings=0',
             'GATES CAPITAL MANAGEMENT, INC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1312908&owner=exclude&count=40&hidefilings=0',
             'GLENVIEW CAPITAL MANAGEMENT, LLC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1138995&owner=exclude&count=40&hidefilings=0',
             'HOUND PARTNERS, LLC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1353316&owner=exclude&count=40&hidefilings=0',
             'ICAHN CARL C': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=921669&owner=exclude&count=40&hidefilings=0',
             'JANA PARTNERS LLC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1159159&owner=exclude&count=40&hidefilings=0',
             'JOHO CAPITAL LLC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1106500&owner=exclude&count=40&hidefilings=0',
             'LONE PINE CAPITAL LLC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1061165&owner=exclude&count=40&hidefilings=0',
             'MARCATO CAPITAL MANAGEMENT LP': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1541996&owner=exclude&count=40&hidefilings=0',
             'OMEGA ADVISORS INC.': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=898202&owner=exclude&count=40&hidefilings=0',
             'PENNANT CAPITAL MANAGEMENT, LLC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1168664&owner=exclude&count=40&hidefilings=0',
             'PERRY CAPITAL': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=919085&owner=exclude&count=40&hidefilings=0',
             'PERSHING SQUARE CAPITAL MANAGEMENT, L.P.': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1336528&owner=exclude&count=40&hidefilings=0',
             'RA CAPITAL MANAGEMENT, LLC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1346824&owner=exclude&count=40&hidefilings=0',
             'RUANE, CUNNIFF & GOLDFARB INC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=85624&owner=exclude&count=40&hidefilings=0',
             'SOROS FUND MANAGEMENT LLC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1029160&owner=exclude&count=40&hidefilings=0',
             'SOUTHEASTERN ASSET MANAGEMENT INC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=807985&owner=exclude&count=40&hidefilings=0',
             'SPO ADVISORY CORP': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=919468&owner=exclude&count=40&hidefilings=0',
             'STARBOARD VALUE LP': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1517137&owner=exclude&count=40&hidefilings=0',
             'TCI FUND MANAGEMENT LTD': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1647251&owner=exclude&count=40&hidefilings=0',
             'TIGER GLOBAL MANAGEMENT LLC': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1167483&owner=exclude&count=40&hidefilings=0',
             'TRIAN FUND MANAGEMENT, L.P.': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1345471&owner=exclude&count=40&hidefilings=0',
             'VIKING GLOBAL INVESTORS LP': 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1103804&owner=exclude&count=40&hidefilings=0'}
