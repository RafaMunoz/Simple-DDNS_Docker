# Simple-DDNS - Docker

The following Docker image will help you easily implement a **DDNS** system in your infrastructure.

You can also configure it for every time the IP address is updated you receive a notification through a Telegram bot.

# How works 
On its first start it will check the Public IP address through the [Ipify API](https://www.ipify.org/) and update the 
IP in your DDNS provider. Every **5 seconds** it will check this IP again and will only update if it changes. 
If you have configured Telegram notifications you can receive a notification every time it is modified.

An example of the request made by the container to update the IP is the following:
 > https://user:password@dyndns.myprovider.com/nic/update?hostname=n01.mydomain.es&myip=%IP%

# Get Started

## Environment variables
Below you can see the Environment variables necessary for the operation of this container.

 - **DOMAINS** -> Domain or list of domains separated by commas. `Example: n01.mydomain.es,n02.mydomain.es`
 - **URL_DDNS** -> URL of your DDNS provider on which requests to update the IP will be made. `Example: dyndns.strato.com`
 - **USERNAME** -> User to authenticate with your DDNS provider.
 - **PASSWORD** -> Password to authenticate with your DDNS provider.
 
 
 ### Optional
 - **TELEGRAM_TOKEN** -> Token of your Telegram bot. 
 - **ID_TELEGRAM**	-> Your Telegram ID to which the messages will be sent.
 
## Start the Container

An example to launch the container could be the following (don't forget to update with your data):

    docker run -d --restart unless-stopped \
    -e "DOMAINS=n01.mydomain.es,n02.mydomain.es" \
    -e "URL_DDNS=dyndns.strato.com" \
    -e "USERNAME=myusername" \
    -e "PASSWORD=mypassword"
    -e "TELEGRAM_TOKEN=378572660:AAHaLn4NylzJuv4kl4XusEtG3L" \
    -e "ID_TELEGRAM=123456" \
    rafa93m/simple-ddns

