#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3

def analyze_photo(photo, verbose=False):

    # Init boto3 Rekognition client
    client = boto3.client('rekognition')

    # Analyse photo => Labels
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
    
    # Debug print statements
    if verbose:
        print('Detected labels in ' + photo)

        for label in response['Labels']:
            print (label['Name'] + ' : ' + str(label['Confidence']))

    persons = list(filter(lambda label : label['Name'] == 'Person', response['Labels']))
    party = list(filter(lambda label : label['Name'] == 'Party', response['Labels']))
    
    return {
        'persons': len(persons[0]['Instances']) if len(persons) > 0 else 0,
        'party': party[0]['Confidence'] if len(party) > 0 else 0
    }

def main(photo):
    print(analyze_photo(photo, verbose=True))


if __name__ == "__main__":
    import sys

    main(sys.argv[1])