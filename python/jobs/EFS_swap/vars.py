host={'B2':'sud-vot-nwsa11app.delta.sbrf.ru','B5':'sud-vot-nwsa21app.delta.sbrf.ru'}
config={
  "NT2": {
    "1.0": {
      "ufs.baseurl.eribsessioninfo": {
        "filtr": {
          "SEGMENT": "PRIVATE",
          "SECTOR": "PRO-SBOL",
          "FIELD": "p2",
          "SUBSYSTEM": "SM_UKO"
        },
        "value": "http://10.106.110.67:9080"
      },
      "erib.rest.limitsexec.path": {
        "value": "10.106.108.69:9080/ERIBRouter/erib/limits/exec"
      },
      "p2bpayment.erib.url": {
        "value": "http://10.106.108.69:9080"
      }
    },
    "2.0": {
      "ufs.baseurl.eribsessioninfo": {
        "tenant_code": "SBOL",
        "filtr": {
          "SUBSYSTEM": "SM_UKO",
          "CHANNEL": ""
        },
        "value": "http://10.106.110.67:9080"
      }
    }
  },
  "NT1": {
    "1.0": {
      "ufs.baseurl.eribsessioninfo": {
        "filtr": {
          "SEGMENT": "PRIVATE",
          "SECTOR": "PRO-SBOL",
          "FIELD": "p2",
          "SUBSYSTEM": "SM_UKO"
        },
        "value": "http://nt2-nlb-dp.testonline.sberbank.ru:10000"
      },
      "erib.rest.limitsexec.path": {
        "value": "10.106.108.69:9080/ERIBRouter/erib/limits/exec"
      },
      "p2bpayment.erib.url": {
        "value": "http://host:port"
      }
    },
    "2.0": {
      "ufs.baseurl.eribsessioninfo": {
        "tenant_code": "SBOL",
        "filtr": {
          "SUBSYSTEM": "SM_UKO",
          "CHANNEL": ""
        },
        "value": "http://10.106.110.105:9080"
      }
    }
  }
}


block=['B2','B5']
stend=['NT2','NT1']
