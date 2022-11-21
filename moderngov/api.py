"""
Module to retrieve data from moderngov api
"""
from itertools import chain
import logging
import requests
import xmltodict
import validators
import re
from diskcache import Cache

logger = logging.getLogger(__name__)

cache = Cache('mgq.cache-dir')


class ModerngovApi:
    """ Handle moderngov API communications """

    def __init__(self, site_url):
        self.site_url = self.clean_url(site_url)

    def clean_url(self, url):
        """ Make sure we have a clean endpoint to talk to """

        if not re.match('^http', url):
            url = f"https://{url}"

        full_url = url + '/mgWebService.asmx'
        self.validate_url(full_url)
        return full_url

    def validate_url(self, url):
        if not validators.url(url):
            logger.error("Not a valid url: %s", url)
            exit(1)

        return True

    @cache.memoize(expire=3600 * 24)
    def get(self, endpoint, params=None):
        """ Get data from the remote endpoint """
        url = self.site_url + "/" + endpoint
        logger.debug("Fetch %s", url)
        try:
            resp = requests.get(url, params, timeout=10, verify=True)
            if resp.status_code == 200:
                return self.convert_xml_to_json(resp.content)
            logger.warning("%s error from %s", resp.status_code, url)
        except Exception as e:
            logger.error("Failed to connect to %s: %s", url, e)
            exit(1)
        else:
            exit(1)

    @staticmethod
    def convert_xml_to_json(data):
        """ Convert the XML received from the remote end to a local useable dict """
        return xmltodict.parse(data, force_list={'meeting', 'linkeddoc', 'attendee', 'agendaitem'})

    def get_councillors_by_ward(self):
        """ Receive from endpoint """
        data = self.get('GetCouncillorsByWard')
        return data["councillorsbyward"]["wards"]["ward"]

    def get_meetings(self, committee_id="0", from_date="0", to_date="0"):
        """ Receive from endpoint """
        params = {"lCommitteeId": committee_id, "sFromDate": from_date, "sToDate": to_date}
        data = self.get('GetMeetings', params)
        return data['getmeetings']["committee"]

    def get_meeting(self, meeting_id):
        """ Receive from endpoint """
        data = self.get('GetMeeting', {"lMeetingId": meeting_id})
        return data

    def get_committees(self):
        """ Receive from endpoint """
        data = self.get('GetCommittees')
        return data['committees']['committee']

    def get_committees_by_member(self, member_id):
        """ Receive from endpoint """
        data = self.get('GetCommitteesByUser', {"lUserId": member_id})
        return data

    def get_member_group(self):
        """ Receive from endpoint """
        data = self.get('GetMemberGroup', {"sOrder": "", "sShortName": ""})
        return data["memberlist"]["members"]["member"]

    @property
    def councillors(self):
        """ Pass to local handler """
        return Councillors(self)

    @property
    def wards(self):
        """ Pass to local handler """
        return Wards(self)

    @property
    def members(self):
        """ Pass to local handler """
        return Members(self)

    @property
    def committees(self):
        """ Pass to local handler """
        return Committees(self)

    @property
    def meetings(self):
        """ Pass to local handler """
        return Meetings(self)


class Councillors:
    """ Councillor specific queries """

    def __init__(self, api: ModerngovApi):
        self.api = api

    def list(self):
        """ List all councillors """
        lst = list(map(lambda x: x["councillors"]["councillor"], self.api.get_councillors_by_ward()))
        flat_list = list(chain(*lst))
        return flat_list

    def by_ward(self):
        """ List all councillors by ward """
        return self.api.get_councillors_by_ward()


class Wards:
    """ Ward specific queries """

    def __init__(self, api: ModerngovApi):
        self.api = api

    def list(self):
        """ get a list of all wards """
        return list(map(lambda x: x["wardtitle"], self.api.get_councillors_by_ward()))


class Members:
    """ Member specific queries """

    def __init__(self, api: ModerngovApi):
        self.api = api

    def list(self):
        """ get a list of all members """
        data = self.api.get_member_group()
        return data

    def by_id(self, member_id: int):
        """ get a member by id """
        data = list(filter(lambda x: int(x['memberid']) == member_id, self.api.get_member_group()))
        if not data:
            return {}
        return data[0]


class Committees:
    """ Committee specific queries """

    def __init__(self, api: ModerngovApi):
        self.api = api

    def list(self):
        """ get a list of all committees """
        return self.api.get_committees()

    def by_member(self, member_id):
        """ get a list of committees the given member id is a member of """
        return self.api.get_committees_by_member(member_id=member_id)

    def by_id(self, committee_id: int):
        """ get a list of committees the given member id is a member of """
        data = list(filter(lambda x: int(x['committeeid']) == committee_id, self.api.get_committees()))
        if not data:
            return {}
        return data[0]


class Meetings:
    """ Meeting specific queries """

    def __init__(self, api: ModerngovApi):
        self.api = api

    def list(self):
        """ get a full list of meetings """
        return self.api.get_meetings()

    def by_meeting_id(self, meeting_id):
        """ get a specific meeting by id """
        return self.api.get_meeting(meeting_id)

    def by_committee_id(self, committee_id):
        """ get all meetings for a given committee """
        return self.api.get_meetings(committee_id=committee_id)
