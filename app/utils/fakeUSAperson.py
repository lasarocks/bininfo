

from faker import Faker

from faker.providers.address.en_US import Provider as AddressProvider



class FakePesonCheckoutAluvii(object):
    def __init__(
        self,
        locale='en_US'
    ):
        self.inst_fake = Faker(locale)
        self.inst_fake.add_provider(ProvedorParser)
        self.full_name = None
        self.first_name = None
        self.last_name = None
        self.street = None
        self.state = None
        self.state_abbr = None
        self.city = None
        self.zipcode = None
        self.email = None
        self.phone = None
        self.person_data = None
        self.gen()
    def gen(self):
        person_data = self.inst_fake.gibe_me_new_person()
        name_data = person_data.get('name_data', {})
        address_data = person_data.get('address_data', {})
        self.full_name = name_data.get('name', '')
        self.first_name = name_data.get('first_name', '')
        self.last_name = name_data.get('last_name', '')
        self.street = address_data.get('street', '')
        self.state = address_data.get('state', '')
        self.state_abbr = address_data.get('state_abbr', '')
        self.zipcode = address_data.get('zipcode', '')
        self.city = address_data.get('city', '')
        self.email = person_data.get('email_data', '')
        self.phone = person_data.get('phone_data', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        self.person_data = person_data








class ProvedorParser(AddressProvider):
    states_with_abbr = [
        {
            "state": "Alabama",
            "state_abbr": "AL"
        },
        {
            "state": "Alaska",
            "state_abbr": "AK"
        },
        {
            "state": "Arizona",
            "state_abbr": "AZ"
        },
        {
            "state": "Arkansas",
            "state_abbr": "AR"
        },
        {
            "state": "California",
            "state_abbr": "CA"
        },
        {
            "state": "Colorado",
            "state_abbr": "CO"
        },
        {
            "state": "Connecticut",
            "state_abbr": "CT"
        },
        {
            "state": "Delaware",
            "state_abbr": "DE"
        },
        {
            "state": "District of Columbia",
            "state_abbr": "DC"
        },
        {
            "state": "Florida",
            "state_abbr": "FL"
        },
        {
            "state": "Georgia",
            "state_abbr": "GA"
        },
        {
            "state": "Hawaii",
            "state_abbr": "HI"
        },
        {
            "state": "Idaho",
            "state_abbr": "ID"
        },
        {
            "state": "Illinois",
            "state_abbr": "IL"
        },
        {
            "state": "Indiana",
            "state_abbr": "IN"
        },
        {
            "state": "Iowa",
            "state_abbr": "IA"
        },
        {
            "state": "Kansas",
            "state_abbr": "KS"
        },
        {
            "state": "Kentucky",
            "state_abbr": "KY"
        },
        {
            "state": "Louisiana",
            "state_abbr": "LA"
        },
        {
            "state": "Maine",
            "state_abbr": "ME"
        },
        {
            "state": "Maryland",
            "state_abbr": "MD"
        },
        {
            "state": "Massachusetts",
            "state_abbr": "MA"
        },
        {
            "state": "Michigan",
            "state_abbr": "MI"
        },
        {
            "state": "Minnesota",
            "state_abbr": "MN"
        },
        {
            "state": "Mississippi",
            "state_abbr": "MS"
        },
        {
            "state": "Missouri",
            "state_abbr": "MO"
        },
        {
            "state": "Montana",
            "state_abbr": "MT"
        },
        {
            "state": "Nebraska",
            "state_abbr": "NE"
        },
        {
            "state": "Nevada",
            "state_abbr": "NV"
        },
        {
            "state": "New Hampshire",
            "state_abbr": "NH"
        },
        {
            "state": "New Jersey",
            "state_abbr": "NJ"
        },
        {
            "state": "New Mexico",
            "state_abbr": "NM"
        },
        {
            "state": "New York",
            "state_abbr": "NY"
        },
        {
            "state": "North Carolina",
            "state_abbr": "NC"
        },
        {
            "state": "North Dakota",
            "state_abbr": "ND"
        },
        {
            "state": "Ohio",
            "state_abbr": "OH"
        },
        {
            "state": "Oklahoma",
            "state_abbr": "OK"
        },
        {
            "state": "Oregon",
            "state_abbr": "OR"
        },
        {
            "state": "Pennsylvania",
            "state_abbr": "PA"
        },
        {
            "state": "Puerto Rico",
            "state_abbr": "PR"
        },
        {
            "state": "Rhode Island",
            "state_abbr": "RI"
        },
        {
            "state": "South Carolina",
            "state_abbr": "SC"
        },
        {
            "state": "South Dakota",
            "state_abbr": "SD"
        },
        {
            "state": "Tennessee",
            "state_abbr": "TN"
        },
        {
            "state": "Texas",
            "state_abbr": "TX"
        },
        {
            "state": "Utah",
            "state_abbr": "UT"
        },
        {
            "state": "Vermont",
            "state_abbr": "VT"
        },
        {
            "state": "Virginia",
            "state_abbr": "VA"
        },
        {
            "state": "Washington",
            "state_abbr": "WA"
        },
        {
            "state": "West Virginia",
            "state_abbr": "WV"
        },
        {
            "state": "Wisconsin",
            "state_abbr": "WI"
        },
        {
            "state": "Wyoming",
            "state_abbr": "WY"
        }
    ]
    email_providers = [
        '@yahoo.com',
        '@aol.com',
        '@icloud.com',
        '@outlook.com'
    ]
    city_formats = (
        '{{city_prefix}} {{first_name}}{{city_suffix}}', '{{city_prefix}} {{first_name}}', '{{first_name}}{{city_suffix}}', '{{last_name}}{{city_suffix}}'
    )
    def fixed_address(self):
        state_rnd = self.generator.random_element(ProvedorParser.states_with_abbr)
        zipcode_wrap = self.generator.postcode_in_state(state_abbr=state_rnd.get('state_abbr', 'NY'))
        street_wrap = self.generator.street_address()
        city_wrap = self.generator.city()
        return {
            'state': state_rnd.get('state', ''),
            'state_abbr': state_rnd.get('state_abbr', ''),
            'zipcode': zipcode_wrap,
            'street': street_wrap,
            'city': city_wrap
        }
    def name_handle(self):
        name_data = self.generator.name()
        name_data_split = name_data.split(' ')
        if len(name_data_split)!=2:
            return self.name_handle()
        for name in name_data_split:
            if len(name)<=3:
                return self.name_handle()
        return {
            'name': name_data,
            'first_name': name_data_split[0].strip(),
            'last_name': name_data_split[1].strip()
        }
    def email_by_name(self, name):
        email_user = name.lower().replace(' ', '.')
        email_host = self.generator.random_element(ProvedorParser.email_providers)
        return f'{email_user}{email_host}'
    def gibe_me_new_person(self):
        name_data = self.name_handle()
        email_data = self.email_by_name(name=name_data.get('name', ''))
        address_data = self.fixed_address()
        return {
            'name_data': name_data,
            'email_data': email_data,
            'address_data': address_data,
            'phone_data': self.generator.basic_phone_number()
        }






