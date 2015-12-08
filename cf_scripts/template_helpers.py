__author__ = '562474'

from troposphere.ec2 import VolumeAttachment,Volume,Instance
from troposphere import AWS_REGION,FindInMap, Ref, GetAtt,constants

import mappings


def volumeAttachment_helper(volume,instance, device='/dev/xvdb'):

    return VolumeAttachment(volume.title+"Attachment",
                                 InstanceId=Ref(instance),
                                 VolumeId=Ref(volume),
                                 Device=device)


def create_and_attach_volume(template,title, instance,device='/dev/xvdb', **kwargs):
    """

    :param template: Reference to the Template
    :param title:  Name of VOlume which will be appended to Instance Name
    :param instance: Instance teh volume will be attahed to
    :param device: Device name of volume, eg /dev/xvdb
    :param kwargs: Keyword arguments that are passed to the Volume Consctructor
    :return:
    """
    # if 'VolumeType' not in kwargs:
    #     kwargs['VolumeType']="gp2"
    if 'Size' not in kwargs:
        kwargs['Size']=str(20)
    if type(kwargs['Size']) is not basestring:
        kwargs['Size']=str(kwargs['Size'])
    if 'AvailabilityZone' not in kwargs:
        kwargs['AvailabilityZone'] = GetAtt(instance,'AvailabilityZone')
    v = template.add_resource(Volume(instance.title+title,**kwargs ))
    return template.add_resource(volumeAttachment_helper(v,instance,device))

