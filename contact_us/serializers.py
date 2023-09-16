from rest_framework.fields import Field

from core.serializers import CustomImageSerializer

class OfficesSerializer(Field):
    def to_representation(self, value):
        if value and len(value) > 0:
            offices = []
            for office in value:
                print(office)
                office_data = office.value
                office_info = {
                    "office_name": office_data.get('office_name'),
                    "address": office_data.get('address').source,
                    "working_hours": office_data.get('working_hours').source,
                    "email": office_data.get('email'),
                    "phone_number": office_data.get('phone_number'),
                    "skype_address": office_data.get('skype_address'),
                    "longitude": office_data.get('longitude'),
                    "latitude": office_data.get('latitude'),
                    "image": CustomImageSerializer().to_representation(office_data.get('image')),
                }
                offices.append(office_info)
            return offices
        return None