config={
  "NT1": {
    "start_on_node": "tvsi-erib0001",
    "jdk_path": "C:\\Program Files\\Java\\jdk1.8.0_191\\bin\\keytool.exe",
    "keystore_path": "D:\\pmi\\pmi\\conf\\ERIB_WAS_trust_store.jks",
    "trust_store_path": "conf/ERIB_WAS_trust_store.jks",
    "trust_store_password": secret,
    "config_path": "D:\\pmi\\pmi\\conf\\config.xml",
    "url": "http://tvli-erib0703:8086/",
    "database": "PMIMetrics",
    "stand": "NT1",
    "certs": "\\certs\\",
    "service_name": "pmi"
  },
  "NT2": {
    "start_on_node": "tvsi-erib0052",
    "jdk_path": "C:\\Program Files\\Java\\jdk1.8.0_191\\bin\\keytool.exe",
    "keystore_path": "D:\\pmi\\pmi\\conf\\ERIB_WAS_trust_store.jks",
    "trust_store_path": "conf/ERIB_WAS_trust_store.jks",
    "trust_store_password": secret,
    "config_path": "D:\\pmi\\pmi\\conf\\config.xml",
    "url": "http://tvli-erib0702:8086/",
    "database": "PMIMetrics",
    "stand": "NT2",
    "certs": "\\certs\\",
    "service_name": "pmi"
  },
  "NT3": {
    "start_on_node": "tvsi-erib0052",
    "jdk_path": "C:\\Program Files\\Java\\jdk1.8.0_191\\bin\\keytool.exe",
    "keystore_path": "D:\\pmi\\pmi_nt3\\conf\\ERIB_WAS_trust_store.jks",
    "trust_store_path": "conf/ERIB_WAS_trust_store.jks",
    "trust_store_password": secret,
    "config_path": "D:\\pmi\\pmi_nt3\\conf\\config.xml",
    "url": "http://tvli-erib0702:8086/",
    "database": "PMIMetrics_nt3",
    "stand": "NT3",
    "certs": "\\certs\\",
    "service_name": "pmi_nt3"
  }
}
if stend=='NT1' or stend=='ALL':
    run_job("configure_pmi", config['NT1'],wait=False)
if stend=='NT2' or stend=='ALL':
    run_job("configure_pmi", config['NT2'],wait=False)
if stend=='NT3' or stend=='ALL':
    run_job("configure_pmi", config['NT3'],wait=False)