Cloud Foundry Deployment
========================

__Note:__ This example is for the commercial pivotal cloud foundry using the `searchly` service.

1. create the elasticsearch service (if it doesnt exist)

    ```
    cf create-service searchly starter
    ```

2. push your app to cloudfoundry

    __Note:__ Adjust the yaml file as needed.

    ```yaml
    applications:
    - name: changeme
    services:
        - changeme
    ```

    ```bash
    cf push -f cf/pcf_example.yml -c "bash ./cf/init.sh"
    ```

3. access your app at __${app_name}.cfapps.io__

4. Future updates only run the following command:

  ```bash
  cf push -f cf/pcf_example.yml
  ```   
