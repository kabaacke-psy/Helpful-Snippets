import pandas as pd
import boto3
import os
import numpy as np
sep = os.path.sep
source_path = os.path.dirname(os.path.abspath(__file__)) + sep
#subjects = pd.read_csv()


def assess_available_data(client, files, subjects):
  '''
    Searches within the hcp1200 release for files matching those int he specified list
    Prints an output with the total number of subjects who have all of the specified files, the average total file size per subject.
    Returns a dictionary with 'Total Search Size'(int, bytes), 'Complete Subject Search Size'(int, bytes), 'Size Per Subject'(list(int, bytes)), 'Size Per Complete Subject'(list(int, bytes)), and 'Complete Subjects'(list(str))
    Args:
      client    (boto3.client): should contain credential given by db.connectome.org
      files     (list(str)) of file patterns to check for. should be a pattern containing the key {subject}
      subjects  (list(str)) list of subjects to check within
  '''
  total_size = 0
  complete_size = 0
  size_per_subject = []
  complete_size_per_subject = []
  subjects_with_complete_data = []
  for sub in subjects:
    sub_filesize = 0
    is_complete = True
    for f in files:
      file_key = f.format(sub)
      if file_key[-1] == '*':
        try:
          sub_response = client.list_objects_v2(
            Bucket='hcp-openaccess',
            Prefix = file_key[:-1]
            )
          for k in sub_response['Contents']:
            sub_filesize += k['Size']
            total_size += k['Size']
        except:
          is_complete = False
      else:
        try:
          k = client.head_object(Bucket='hcp-openaccess',Key=file_key)
          sub_filesize += k['ContentLength']
          total_size += k['ContentLength']
        except:
          is_complete = False
    if is_complete:
      subjects_with_complete_data.append(sub)
      complete_size += sub_filesize
      complete_size_per_subject.append(sub_filesize)
    size_per_subject.append(sub_filesize)
    print(sub, sub_filesize/10**9, 'GB')
  print('Total size of all files mathcing patterns: ' + str(total_size/10**9) + ' GB')
  print('Average file size per subject: ' + str(np.mean(size_per_subject)/10**9) + ' GB')
  print('Number of subjects with all target files: ' + str(len(subjects_with_complete_data)))
  print('Total size of files within subjects with the complete set of files: ' + str(complete_size/10**9) + ' GB')
  print('Average folder size per complete subject: ' + str(np.mean(complete_size_per_subject)/10**9) + ' GB')
  return {
    'Total Search Size':total_size,
    'Complete Subject Search Size':complete_size,
    'Size Per Subject':size_per_subject,
    'Size Per Complete Subject':complete_size_per_subject,
    'Complete Subjects':subjects_with_complete_data
  }

if __name__ == '__main__':
  cred = pd.read_csv(sep+'Users'+sep+'kyle'+sep+'repos'+sep+'HCP-Task-Classification-01'+sep+'misc'+sep+'kp.csv') 
  subjects = pd.read_csv(sep+'Users'+sep+'kyle'+sep+'repos'+sep+'HCP-Task-Classification-01'+sep+'subject_list.csv')['ID']
  hcp_s3_c = boto3.client(
    's3',
    region_name='us-east-2',
    aws_access_key_id=cred['Access key ID'][1],
    aws_secret_access_key=cred['Secret access key'][1]
    )
  hcp_s3_r = boto3.resource( 
    's3',
    region_name='us-east-2',
    aws_access_key_id=cred['Access key ID'][1],
    aws_secret_access_key=cred['Secret access key'][1])
  
  # Seach for and assess the size of a subset of files within hcp_openaccess
  if True:
    target_files = [
      'HCP_1200/{}/.xdlm/*',
      'HCP_1200/{}/MNINonLinear/*',
      'HCP_1200/{}/T1w/*',
      'HCP_1200/{}/release-notes/*',
      'HCP_1200/{}/unprocessed/*', #36405.798214824 GB not including all above
      'HCP_1200/{}/MEG/*' # 37645.204332495 GB including all above, 95 with MEG folders
    ]
    #subjects = hcp1200_subjects
    search_dict = assess_available_data(hcp_s3_c, target_files, subjects)

  # Determine size of the full hcp1200 release on openaccess 88574.889 GB
  if False:
    # option1
    # hcp1200_size = 0
    # for obj in hcp_s3_c.list_objects_v2(Bucket='hcp-openaccess', Prefix ='HCP_1200/')['Contents']:
    #   hcp1200_size += obj['size']
    # print('Total HCP1200 release filesize: ' + str(hcp1200_size/10**9) + ' GB')
    #option2
    hcp1200_size = 0
    hcp1200 = hcp_s3_r.Bucket('hcp-openaccess')
    for obj in hcp1200.objects.filter(Prefix='HCP_1200/'):
      hcp1200_size += obj.size

  # Search to count subjects with a 7T sub-directory
  if True: # 184 Subjects with 7T data
    target_list = []
    for subject in subjects:
        pref = 'HCP_1200/'+str(subject)+'/unprocessed/7T/'
        response = hcp_s3_c.list_objects_v2(
                    Bucket='hcp-openaccess',
                    Prefix = pref
                    )
        try:
            if len(response['Contents'])>1:
                target_list.append(subject)
        except:
            pass
        
        '''
        print('Objects per Subject:')
        total_size = 0
        for obj in response['Contents']:
            gb_size = str(round(obj['Size']/10**9, 4))
            print(f'  {gb_size} GB - {obj["Key"]}')
            total_size += obj['Size']
        print('Total Size: ' + str(total_size/10**9) + ' GB')
        '''
    print(str(len(target_list)) + ' subjects have 7T folders.')

  # Search to determine the total filesize of all 3T and 7T unprocessed data
  if False:
    full_total = 0
    for subject in target_list:
        response1 = hcp_s3_c.list_objects_v2(
                    Bucket='hcp-openaccess',
                    Prefix ='HCP_1200/'+str(subject)+'/unprocessed/3T/'
                    )
        #print('Objects per Subject:')
        print("Subject " + str(subject))
        total_size = 0
        for obj in response1['Contents']:
            gb_size = str(round(obj['Size']/10**9, 4))
            #print(f'  {gb_size} GB - {obj["Key"]}')
            total_size += obj['Size']
            full_total += obj['Size']

        response2 = hcp_s3_c.list_objects_v2(
                    Bucket='hcp-openaccess',
                    Prefix ='HCP_1200/'+str(subject)+'/unprocessed/7T/'
                    )
        for obj in response2['Contents']:
            gb_size = str(round(obj['Size']/10**9, 4))
            if 'PHYSIO' in obj["Key"]:
                print("This one has physio 7T data.")
            #print(f'  {gb_size} GB - {obj["Key"]}')
            total_size += obj['Size']
            full_total += obj['Size']

        print('Participant file size: ' + str(total_size/10**9) + ' GB')
    print('Total Size: ' + str(full_total/10**9) + ' GB')