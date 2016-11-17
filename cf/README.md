Cloud Foundry Deployment
========================

__Note:__ This example is for the commercial pivotal cloud foundry using the `searchly` service.

+ initially create the elasticsearch service (if it doesnt exist)

```bash
cf create-service searchly starter es-dev
```

+ push your app to cloudfoundry

__Note:__ Adjust the name if you need in the yaml file.

```yaml
applications:
- name: CUSTOM_DOMAIN
```

```bash
cf push -f cf/pcf_dev.yml
```

+ access your app at {app_name}.cfapps.io
