import boto3

class Gp2togp3:
    def __init__(self,region):
        self.region=region
        self.ec2_cli=boto3.client('ec2',region_name=region)
        self.instancelist = []
    def convert_volume(self):
        vol=self.ec2_cli.describe_volumes()
        instancelist = []
        print(self.region)
        for each_item in vol['Volumes']:
            if each_item['VolumeType'] == 'gp2':
                #print(each_item['VolumeType'])
                self.instancelist.append(each_item['VolumeId'])
        return self.instancelist
    def print_ids(self):
        for item in self.instancelist:
            print(item)
            print('---------')
    def modify_volume(self):
        for item in self.instancelist:
            self.ec2_cli.modify_volume(VolumeId=item,VolumeType='gp3')
            print(item)
            
def lambda_handler(event, context):
    ec2_cli = boto3.client('ec2')
    response = ec2_cli.describe_regions()
    for each in response['Regions']:
        class_obj=Gp2togp3(each['RegionName'])
        class_obj.convert_volume()
        class_obj.modify_volume()
