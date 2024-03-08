#!/usr/bin/env python3

import argparse
import os.path
import json


def converter_meta(primary_config_d: dict) -> dict:
    try:
        new_config_d = {
            'diffs'           : [{'diff': primary_config_d["diffList"][0]}],
            'groups'          : primary_config_d["taskSampleList"],
            'level'           : None,
            'parameterlist'   : primary_config_d["parameterList"],
            'pipeline'        : primary_config_d["pipeline"],
            'sample'          : primary_config_d["serverInfo"],
            'sampleNumber'    : primary_config_d["sampleNumber"],
            'taskId'          : primary_config_d["taskId"],
            'taskName'        : primary_config_d["taskName"],
            'analysisRecordId': primary_config_d["analysisRecordId"]
        }
        new_config_d['sample']['filePath'] = primary_config_d["rootPath"]
    except Exception as e:
        print(str(e))
        return {}
    return new_config_d


def converter_CNV(primary_config_d: dict) -> dict:
    try:
        new_config_d = {
            'dataType'        : primary_config_d["parameterList"]["Microarray"],
            'genomeVersion'   : primary_config_d["parameterList"]["genome_version"],
            'normalName'      : primary_config_d,
            'normalPath'      : primary_config_d,
            'patientID2'      : primary_config_d["patientId2"],
            'pipeline'        : primary_config_d["pipeline"],
            'taskId'          : primary_config_d["taskId"],
            'taskName'        : primary_config_d["taskName"],
            'tumorName'       : primary_config_d,
            'tumorPath'       : primary_config_d,
            'analysisRecordId': primary_config_d["analysisRecordId"]
        }
        for task_sample in primary_config_d["taskSampleList"]:
            if task_sample['sampleType'] == 'normal':
                new_config_d['normalName'] = task_sample['sampleName']
                new_config_d['normalPath'] = task_sample['fileName']
                continue
            if task_sample['sampleType'] == 'tumor':
                new_config_d['tumorName'] = task_sample['sampleName']
                new_config_d['tumorPath'] = task_sample['fileName']
    except Exception as e:
        print(str(e))
        return {}
    return new_config_d


def converter_16S(primary_config_d: dict) -> dict:
    try:
        new_config_d = {
            'groups'          : primary_config_d["taskSampleList"][0]["groupName"],
            'level'           : None,
            'parameterlist'   : primary_config_d["parameterList"],
            'pipeline'        : primary_config_d["pipeline"],
            'sample'          : primary_config_d["serverInfo"],
            'sampleNumber'    : primary_config_d["sampleNumber"],
            'taskId'          : primary_config_d["taskId"],
            'taskName'        : primary_config_d["taskName"],
            'analysisRecordId': primary_config_d["analysisRecordId"]
        }
        new_config_d['sample']['filePath']        = primary_config_d["rootPath"]
        new_config_d['sample']['metadata']        = primary_config_d["metadata"]
        new_config_d['sample']['metadataContent'] = primary_config_d["metadataContent"]
        new_config_d['sample']['samplenames']     = primary_config_d["samplenames"]
        new_config_d['sample']['userName']        = primary_config_d["serverInfo"]["username"]
    except Exception as e:
        print(str(e))
        return {}
    return new_config_d


def converter_lncRNA(primary_config_d: dict) -> dict:
    try:
        new_config_d = {
            'diffs'           : [{'diff': primary_config_d["diffList"][0]}],
            'groups'          : primary_config_d["taskSampleList"],
            'level'           : None,
            'parameterlist'   : primary_config_d["parameterList"],
            'patientId2'      : primary_config_d["patientId2"],
            'pipeline'        : primary_config_d["pipeline"],
            'sample'          : primary_config_d["serverInfo"],
            'sampleNumber'    : primary_config_d["sampleNumber"],
            'taskId'          : primary_config_d["taskId"],
            'taskName'        : primary_config_d["taskName"],
            'analysisRecordId': primary_config_d["analysisRecordId"]
        }
        new_config_d['sample']['filePath'] = primary_config_d["rootPath"]
    except Exception as e:
        print(str(e))
        return {}
    return new_config_d


def converter_HLA(primary_config_d: dict) -> dict:
    try:
        new_config_d = primary_config_d
        new_config_d['r1Path']     = primary_config_d['taskSampleList'][0]['read1']
        new_config_d['r2Path']     = primary_config_d['taskSampleList'][0]['read2']
        new_config_d['sampleName'] = primary_config_d['taskSampleList'][0]['sampleName']
    except Exception as e:
        print(str(e))
        return {}
    return new_config_d


def converter_smallRNA(primary_config_d: dict) -> dict:
    try:
        new_config_d = primary_config_d
        new_config_d['patientID2'] = primary_config_d['patientId2']
        for sample_content in primary_config_d['taskSampleList']:
            if sample_content['sampleType'].strip().lower() == 'tumor':
                new_config_d['tumorName'] = sample_content['sampleName']
                new_config_d['tumorPath'] = sample_content['faFile']
                continue
            else:
                pass
            if sample_content['sampleType'].strip().lower() == 'normal':
                new_config_d['normalName'] = sample_content['sampleName']
                new_config_d['normalPath'] = sample_content['faFile']
                continue
            else:
                pass
    except Exception as e:
        print(str(e))
        return {}
    return new_config_d


def steward(primary_config:str) -> int:
    work_dir = os.path.dirname(primary_config)
    try:
        with open(primary_config) as primary_config_f:
            primary_config_d = json.load(primary_config_f)
        pipeline_name = primary_config_d['pipeline']
    except KeyError as e:
        print(str(e))
    if pipeline_name == 'metabonomics':
        new_config_d = converter_meta(primary_config_d)
    elif pipeline_name == 'CNV':
        new_config_d = converter_CNV(primary_config_d)
    elif pipeline_name == '16S_rRNA':
        new_config_d = converter_16S(primary_config_d)
    elif pipeline_name == 'lncRNA':
        new_config_d = converter_lncRNA(primary_config_d)
    elif pipeline_name == 'HLA':
        new_config_d = converter_HLA(primary_config_d)
    elif pipeline_name == 'smallRNA':
        new_config_d = converter_smallRNA(primary_config_d)
    else:
        return 1
    if len(new_config_d) == 0:
        return 1
    else:
        os.rename(primary_config, primary_config + '.origin')
        with open(primary_config, 'w') as out_f:
            json.dump(new_config_d, out_f, ensure_ascii=False, indent=4)
        return 0

def main() -> None:
    parser = argparse.ArgumentParser(description='convert the 3rd config file to the 2nd config file')
    parser.add_argument('-c', '--config', required=True, help='the 3rd config file with full path')
    args = parser.parse_args()
    primary_config = args.config
    if os.path.isabs(primary_config):
        pass
    else:
        primary_config = os.path.abspath(os.path.basename(primary_config))
    result_status = steward(primary_config)
    if result_status == 0:
        print('Done')
    else:
        print('Error')

if __name__ == '__main__':
    main()