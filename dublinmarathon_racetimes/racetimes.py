
import optparse
import mechanize
import re
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

class RaceTimes():

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop("name", None)

    def grabRaceTimes(self):
        url = 'http://results.dublinmarathon.ie/results.php'
        browser = Browser()
        browser.set_handle_robots(False)
        browser.open(url)

        browser.select_form(nr=0)

        control = browser.form.find_control("race")

        all_races = [{'id': item.attrs['value'],'label': item.attrs['label']} for item in control.items]
        all_races.reverse()

        print '{_race:<50} {_place_overall:<15} {_name:<35} {_from:<20} {_category:<10} {_place_in_category:<20} {_chip_time:<13} {_finish_time:>13} - Marathon Only {_10km_time:>10} {_1st_half_time:>10} {_30km_time:>10}'.format(_race='Race', _place_overall='Place overall', _name='Name', _from='From', _category='Category', _place_in_category='Place in category', _chip_time='Chip time', _finish_time='Finish time', _10km_time='10km', _1st_half_time='21km',_30km_time='30km'  )

        for selected_race in all_races:
            browser.open(url)
            browser.select_form(nr=0)
            selected_race_id = selected_race['id']

            browser['name'] = self.name
            browser['race'] = [selected_race_id]#['29']#
            response = browser.submit()
            content = response.read()

            bcontent = BeautifulSoup(content)
            results_table = bcontent.findAll('table', attrs={"class" : 'results_table'})


            if len(results_table) > 0:
                result_list = results_table[0].findAll('tr')
                if len(result_list) > 1:#first one is the table headers
                    result_list.pop(0)

                    for result in result_list:
                        result_breakdown = result.findAll('td')
                        _race = selected_race['label']
                        _place_overall = result_breakdown[0].text
                        _name = result_breakdown[1].text
                        _from = result_breakdown[2].text
                        _category = result_breakdown[3].text
                        _place_in_category = result_breakdown[4].text


                        if len(result_breakdown)==10:#marathon
                            # 10km time
                            _10km_time = result_breakdown[5].text
                            # 1st-half time
                            _1st_half_time = result_breakdown[6].text
                            # 30km time
                            _30km_time = result_breakdown[7].text

                            _chip_time = result_breakdown[8].text
                            _finish_time = result_breakdown[9].text
                        else:
                            _10km_time, _1st_half_time, _30km_time = '','',''
                            _chip_time = result_breakdown[5].text
                            _finish_time = result_breakdown[6].text


                        print '{_race:<50} {_place_overall:<15} {_name:<35} {_from:<20} {_category:<10} {_place_in_category:<20} {_chip_time:<13} {_finish_time:>13} {_10km_time:>26} {_1st_half_time:>10} {_30km_time:>10}'.format(_race=_race, _place_overall=_place_overall, _name=_name, _from=_from, _category=_category, _place_in_category=_place_in_category, _chip_time=_chip_time, _finish_time=_finish_time, _10km_time=_10km_time, _1st_half_time=_1st_half_time,_30km_time=_30km_time )




if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-n', '--name', action='store', type="string", dest='name', default=None,
            help='What name do you want to search?')
    (options, args) = parser.parse_args()


    if not options.name:
        print "Name is required\n"
        parser.print_help()
        exit(-1)
    else:

        name  = options.name
        r = RaceTimes(name=name)
        r.grabRaceTimes()



