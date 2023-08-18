from codeable_models import CClass, add_links, CBundle
from metamodels.component_metamodel import component
from metamodels.microservice_components_metamodel import client, service, restful_http, \
    http, discovery_service, configuration_service, mongo_db, https, external_component, database_connector, \
    monitoring_component, monitoring_dashboard, circuit_breaker, messaging, load_balancer, \
    tracing_component, api_gateway
from security_annotations_metamodel import authentication_scope_all_requests, authentication_with_plaintext_credentials, \
    connector_code_plaintext_sensitive_data, no_authentication, csrf_scope_all_requests, no_csrf_protection, \
    unencrypted_communication, http_basic_authentication, component_code_plaintext_sensitive_data, oauth2_server, \
    auth_provider, token_based_authorization, authorization_scope_all_requests, secure_authentication_token

# Source: https://github.com/sqshq/piggymetrics

# System Component
service_client = CClass(component, "Client", stereotype_instances=client)

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/java/com/piggymetrics/config/ConfigApplication.java

config server

@SpringBootApplication
@EnableConfigServer
public class ConfigApplication {

	public static void main(String[] args) {
		SpringApplication.run(ConfigApplication.class, args);
	}
}

In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/application.yml

config service with plaintext hardcoded password.

spring:
  cloud:
    config:
      server:
        native:
          search-locations: classpath:/shared
  profiles:
     active: native
  security:
    user:
      password: ${CONFIG_SERVICE_PASSWORD}

As explained in:

https://github.com/sqshq/piggymetrics

"An advanced security configuration is beyond the scope of this proof-of-concept project. For a more realistic simulation of a real system, consider to use https, JCE keystore to encrypt Microservices passwords and Config server properties content (see documentation for details)."

-> Config data is sensitive data and is handled as plaintext here.
-> No HTTPs used anywhere (below)
-> Plaintext passwords (sensitive data) on links (below) confirmed, alternative keystore

'''

config = CClass(component, "Config Service",
                stereotype_instances=[configuration_service, component_code_plaintext_sensitive_data])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/gateway/src/main/java/com/piggymetrics/gateway/GatewayApplication.java

@SpringBootApplication
@EnableDiscoveryClient
@EnableZuulProxy
public class GatewayApplication {

	public static void main(String[] args) {
		SpringApplication.run(GatewayApplication.class, args);
	}
	

In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/java/com/piggymetrics/config/SecurityConfig.java
        http.csrf().disable();
        http
            .authorizeRequests()
                .antMatchers("/actuator/**").permitAll()
                .anyRequest().authenticated()
            .and()
                .httpBasic()
                ;
-> CSRF disabled. HTTP Basic auth turned on; all authenticated are authorized


In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/gateway.yml

API Gateway -- ribbon load balancer config

ribbon:
  ReadTimeout: 20000
  ConnectTimeout: 20000

This uses info from Eureka: See
https://github.com/sqshq/piggymetrics

Ribbon

Ribbon is a client side load balancer which gives you a lot of control over the behaviour of HTTP and TCP clients. Compared to a traditional load balancer, there is no need in additional hop for every over-the-wire invocation - you can contact desired service directly.

Out of the box, it natively integrates with Spring Cloud and Service Discovery. Eureka Client provides a dynamic list of available servers so Ribbon could balance between them.


'''

gateway = CClass(component, "Zuul API Gateway",
                 stereotype_instances=[api_gateway, no_csrf_protection, csrf_scope_all_requests, load_balancer])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/gateway/src/main/resources/bootstrap.yml

Links to config service:
  cloud:
    config:
      uri: http://config:8888
      fail-fast: true
      password: ${CONFIG_SERVICE_PASSWORD}
      username: user

using HTTP

sensitive data (password) as plaintext 
'''

add_links({gateway: config},
          role_name="target", stereotype_instances=[restful_http, http, authentication_with_plaintext_credentials,
                                                    authentication_scope_all_requests,
                                                    connector_code_plaintext_sensitive_data])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/gateway.yml

the client routes are configured:

zuul:
  ignoredServices: '*'
  host:
    connect-timeout-millis: 20000
    socket-timeout-millis: 20000

  routes:
    auth-service:
        path: /uaa/**
        url: http://auth-service:5000
        stripPrefix: false
        sensitiveHeaders:

    account-service:
        path: /accounts/**
        serviceId: account-service
        stripPrefix: false
        sensitiveHeaders:

    statistics-service:
        path: /statistics/**
        serviceId: statistics-service
        stripPrefix: false
        sensitiveHeaders:

    notification-service:
        path: /notifications/**
        serviceId: notification-service
        stripPrefix: false
        sensitiveHeaders:

-> this also shows there are four service connected to the API Gateway [*1]
          
'''

add_links({service_client: gateway},
          role_name="target", stereotype_instances=[restful_http, http])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/auth-service/src/main/java/com/piggymetrics/auth/AuthApplication.java

AuthApplication is offered. 

@SpringBootApplication
@EnableResourceServer
@EnableDiscoveryClient
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class AuthApplication {

	public static void main(String[] args) {
		SpringApplication.run(AuthApplication.class, args);
	}

}

In: 
https://github.com/sqshq/piggymetrics/blob/master/auth-service/src/main/java/com/piggymetrics/auth/controller/UserController.java

controller for getting current user and creating users is offered

@RestController
@RequestMapping("/users")
public class UserController {

	@Autowired
	private UserService userService;

	@RequestMapping(value = "/current", method = RequestMethod.GET)
	public Principal getUser(Principal principal) {
		return principal;
	}

	@PreAuthorize("#oauth2.hasScope('server')")
	@RequestMapping(method = RequestMethod.POST)
	public void createUser(@Valid @RequestBody User user) {
		userService.create(user);
	}
}



In:
https://github.com/sqshq/piggymetrics/blob/master/auth-service/src/main/java/com/piggymetrics/auth/service/UserServiceImpl.java

- User information is created with encrypted storage of password
- and stored in a mongodb

private static final BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
...
String hash = encoder.encode(user.getPassword());
		user.setPassword(hash);
		repository.save(user);

In:
https://github.com/sqshq/piggymetrics/blob/master/auth-service/src/main/java/com/piggymetrics/auth/config/OAuth2AuthorizationConfig.java

- authorization of the three services and the browser is configured.
    

        clients.inMemory()
                .withClient("browser")
                .authorizedGrantTypes("refresh_token", "password")
                .scopes("ui")
                .and()
                .withClient("account-service")
                .secret(env.getProperty("ACCOUNT_SERVICE_PASSWORD"))
                .authorizedGrantTypes("client_credentials", "refresh_token")
                .scopes("server")
                .and()
                .withClient("statistics-service")
                .secret(env.getProperty("STATISTICS_SERVICE_PASSWORD"))
                .authorizedGrantTypes("client_credentials", "refresh_token")
                .scopes("server")
                .and()
                .withClient("notification-service")
                .secret(env.getProperty("NOTIFICATION_SERVICE_PASSWORD"))
                .authorizedGrantTypes("client_credentials", "refresh_token")
                .scopes("server");


In:



- sensitive data management with auth data: encrypted

'''

oauth2 = CClass(component, "OAuth2 Server", stereotype_instances=[oauth2_server,
                                                                  component_code_plaintext_sensitive_data])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/application.yml

security:
  oauth2:
    resource:
      user-info-uri: http://auth-service:5000/uaa/users/current

'''

add_links({gateway: oauth2},
          role_name="target", stereotype_instances=[auth_provider, restful_http, http])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/account-service/src/main/java/com/piggymetrics/account/service/AccountServiceImpl.java    
autowired mongo AccountRepository

@Autowired
	private UserRepository repository;


and Repository in:
https://github.com/sqshq/piggymetrics/blob/master/auth-service/src/main/java/com/piggymetrics/auth/repository/UserRepository.java

@Repository
public interface UserRepository extends CrudRepository<User, String> {


In:
https://github.com/sqshq/piggymetrics/blob/master/auth-service/src/main/java/com/piggymetrics/auth/service/security/MongoUserDetailsService.java

autowired mongo user details service


In:
https://github.com/sqshq/piggymetrics/blob/master/docker-compose.yml

  auth-mongodb:
    environment:
      MONGODB_PASSWORD: $MONGODB_PASSWORD
    image: sqshq/piggymetrics-mongodb
    restart: always
    logging:
      options:
        max-size: "10m"
        max-file: "10"
        
mongo db image          

In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/auth-service.yml
spring:
  data:
    mongodb:
      host: auth-mongodb
      username: user
      password: ${MONGODB_PASSWORD}
      database: piggymetrics
      port: 27017
    
plain text credentials for auth mongo db

unencrypted communication (no sign of SSL use)

'''
user_repo = CClass(component, "User Repository", stereotype_instances=[mongo_db])

add_links({oauth2: user_repo},
          role_name="target",
          stereotype_instances=[database_connector, authentication_with_plaintext_credentials,
                                authentication_scope_all_requests,
                                connector_code_plaintext_sensitive_data, unencrypted_communication])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/account-service/src/main/java/com/piggymetrics/account/AccountApplication.java

@SpringBootApplication
@EnableDiscoveryClient
@EnableOAuth2Client
@EnableFeignClients
@EnableCircuitBreaker
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class AccountApplication {

	public static void main(String[] args) {
		SpringApplication.run(AccountApplication.class, args);
	}

}

- Circuit Breaker with Hystrix enabled

In:
https://github.com/sqshq/piggymetrics/blob/master/account-service/src/main/java/com/piggymetrics/account/controller/AccountController.java

Restcontroller

'''
account_service = CClass(component, "Account Service", stereotype_instances=[service, circuit_breaker])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/account-service/src/main/resources/bootstrap.yml

  cloud:
    config:
      uri: http://config:8888
      fail-fast: true
      password: ${CONFIG_SERVICE_PASSWORD}
      username: user

sensitive data (password) as plaintext 
'''

add_links({account_service: config},
          role_name="target", stereotype_instances=[restful_http, http, authentication_with_plaintext_credentials,
                                                    authentication_scope_all_requests,
                                                    connector_code_plaintext_sensitive_data])

'''
In: [*1] 

-> link to API gateway

In:

- if not actuator, authorize all requests
- that are authenticated with basic auth

https://github.com/sqshq/piggymetrics/blob/master/config/src/main/java/com/piggymetrics/config/SecurityConfig.java

        http.csrf().disable();
        http
            .authorizeRequests()
                .antMatchers("/actuator/**").permitAll()
                .anyRequest().authenticated()
            .and()
                .httpBasic()
                ;

'''
add_links({gateway: account_service},
          role_name="target",
          stereotype_instances=[restful_http, http, http_basic_authentication, authentication_scope_all_requests,
                                token_based_authorization,
                                authorization_scope_all_requests])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/account-service/src/main/java/com/piggymetrics/account/service/AccountServiceImpl.java    
autowired mongo AccountRepository

@Autowired
	private AccountRepository repository;

and Repository in:
https://github.com/sqshq/piggymetrics/blob/master/account-service/src/main/java/com/piggymetrics/account/repository/AccountRepository.java

@Repository
public interface AccountRepository extends CrudRepository<Account, String> {


In:
https://github.com/sqshq/piggymetrics/blob/master/docker-compose.yml

  account-mongodb:
    environment:
      INIT_DUMP: account-service-dump.js
      MONGODB_PASSWORD: $MONGODB_PASSWORD
    image: sqshq/piggymetrics-mongodb
    restart: always
    logging:
      options:
        max-size: "10m"
        max-file: "10"  

mongo db image          

In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/auth-service.yml
spring:
  data:
    mongodb:
      host: account-mongodb
      username: user
      password: ${MONGODB_PASSWORD}
      database: piggymetrics
      port: 27017

plain text credentials for auth mongo db

unencrypted communication (no sign of SSL use)

'''
account_repo = CClass(component, "Account Repository", stereotype_instances=[mongo_db])

add_links({account_service: account_repo},
          role_name="target",
          stereotype_instances=[database_connector, authentication_with_plaintext_credentials,
                                authentication_scope_all_requests,
                                connector_code_plaintext_sensitive_data, unencrypted_communication])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/account-service.yml

security:
  oauth2:
    client:
      clientId: account-service
      clientSecret: ${ACCOUNT_SERVICE_PASSWORD}
      accessTokenUri: http://auth-service:5000/uaa/oauth/token
      grant-type: client_credentials
      scope: server

authentication of oauth service uses plain text credentials, sensitive data in the code.

-> would have modelled this as:

add_links({account_service: oauth2},
          role_name="target",
          stereotype_instances=[auth_provider, restful_http, http, authentication_with_plaintext_credentials,
                                authentication_scope_all_requests, connector_code_plaintext_sensitive_data])
                                
but as the link also uses a Feign client, modelled the two below together [*2]

'''

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/notification-service/src/main/java/com/piggymetrics/notification/NotificationServiceApplication.java

@SpringBootApplication
@EnableDiscoveryClient
@EnableOAuth2Client
@EnableFeignClients
@EnableGlobalMethodSecurity(prePostEnabled = true)
@EnableScheduling
public class NotificationServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(NotificationServiceApplication.class, args);
	}


In:
https://github.com/sqshq/piggymetrics/tree/master/notification-service/src/main/java/com/piggymetrics/notification/controller

Restcontroller

'''

notification_service = CClass(component, "Notification Service", stereotype_instances=service)

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/notification-service/src/main/resources/bootstrap.yml
  cloud:
    config:
      uri: http://config:8888
      fail-fast: true
      password: ${CONFIG_SERVICE_PASSWORD}
      username: user

sensitive data (password) as plaintext 
'''

add_links({notification_service: config},
          role_name="target", stereotype_instances=[restful_http, http, authentication_with_plaintext_credentials,
                                                    authentication_scope_all_requests,
                                                    connector_code_plaintext_sensitive_data])

'''
In: [*1] 

-> link to API gateway

In:

- if not actuator, authorize all requests
- that are authenticated with basic auth

https://github.com/sqshq/piggymetrics/blob/master/config/src/main/java/com/piggymetrics/config/SecurityConfig.java

        http.csrf().disable();
        http
            .authorizeRequests()
                .antMatchers("/actuator/**").permitAll()
                .anyRequest().authenticated()
            .and()
                .httpBasic()
                ;

'''
add_links({gateway: notification_service},
          role_name="target",
          stereotype_instances=[restful_http, http, http_basic_authentication, authentication_scope_all_requests,
                                token_based_authorization,
                                authorization_scope_all_requests])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/notification-service/src/main/java/com/piggymetrics/notification/service/RecipientServiceImpl.java
autowired mongo RecipientRepository

@Autowired
	private RecipientRepository repository;

and Repository in:
https://github.com/sqshq/piggymetrics/blob/master/notification-service/src/main/java/com/piggymetrics/notification/repository/RecipientRepository.java

@Repository
public interface RecipientRepository extends CrudRepository<Recipient, String> {


In:
https://github.com/sqshq/piggymetrics/blob/master/docker-compose.yml

  notification-mongodb:
    image: sqshq/piggymetrics-mongodb
    restart: always
    environment:
      MONGODB_PASSWORD: $MONGODB_PASSWORD
    logging:
      options:
        max-size: "10m"
        max-file: "10"

mongo db image          

In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/auth-service.yml
spring:
  data:
    mongodb:
      host: notification-mongodb
      username: user
      password: ${MONGODB_PASSWORD}
      database: piggymetrics
      port: 27017

plain text credentials for auth mongo db

unencrypted communication (no sign of SSL use)

'''
recipient_repo = CClass(component, "Recipient Repository", stereotype_instances=[mongo_db])

add_links({notification_service: recipient_repo},
          role_name="target",
          stereotype_instances=[database_connector, authentication_with_plaintext_credentials,
                                authentication_scope_all_requests,
                                connector_code_plaintext_sensitive_data, unencrypted_communication])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/notification-service.yml

security:
  oauth2:
    client:
      clientId: notification-service
      clientSecret: ${NOTIFICATION_SERVICE_PASSWORD}
      accessTokenUri: http://auth-service:5000/uaa/oauth/token
      grant-type: client_credentials
      scope: server


authentication of oauth service uses plain text credentials, sensitive data in the code.


'''

add_links({notification_service: oauth2},
          role_name="target",
          stereotype_instances=[auth_provider, restful_http, http, authentication_with_plaintext_credentials,
                                authentication_scope_all_requests, connector_code_plaintext_sensitive_data])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/statistics-service/src/main/java/com/piggymetrics/statistics/StatisticsApplication.java

@SpringBootApplication
@EnableDiscoveryClient
@EnableOAuth2Client
@EnableFeignClients
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class StatisticsApplication {

	public static void main(String[] args) {
		SpringApplication.run(StatisticsApplication.class, args);
	}

In:
https://github.com/sqshq/piggymetrics/blob/master/statistics-service/src/main/java/com/piggymetrics/statistics/controller/StatisticsController.java

Restcontroller

'''

statistics_service = CClass(component, "Statistics Service", stereotype_instances=service)

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/statistics-service/src/main/resources/bootstrap.yml
  cloud:
    config:
      uri: http://config:8888
      fail-fast: true
      password: ${CONFIG_SERVICE_PASSWORD}
      username: user

sensitive data (password) as plaintext 
'''

add_links({statistics_service: config},
          role_name="target", stereotype_instances=[restful_http, http, authentication_with_plaintext_credentials,
                                                    authentication_scope_all_requests,
                                                    connector_code_plaintext_sensitive_data])

'''
In: [*1] 

-> link to API gateway

In:

- if not actuator, authorize all requests
- that are authenticated with basic auth

https://github.com/sqshq/piggymetrics/blob/master/config/src/main/java/com/piggymetrics/config/SecurityConfig.java

        http.csrf().disable();
        http
            .authorizeRequests()
                .antMatchers("/actuator/**").permitAll()
                .anyRequest().authenticated()
            .and()
                .httpBasic()
                ;

'''
add_links({gateway: statistics_service},
          role_name="target",
          stereotype_instances=[restful_http, http, http_basic_authentication, authentication_scope_all_requests,
                                token_based_authorization,
                                authorization_scope_all_requests])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/statistics-service/src/main/java/com/piggymetrics/statistics/service/StatisticsServiceImpl.java
autowired mongo DataPointRepository

@Autowired
	private DataPointRepository repository;

and Repository in:
https://github.com/sqshq/piggymetrics/blob/master/statistics-service/src/main/java/com/piggymetrics/statistics/repository/DataPointRepository.java


@Repository
public interface DataPointRepository extends CrudRepository<DataPoint, DataPointId> {

In:
https://github.com/sqshq/piggymetrics/blob/master/docker-compose.yml

  statistics-mongodb:
    environment:
      MONGODB_PASSWORD: $MONGODB_PASSWORD
    image: sqshq/piggymetrics-mongodb
    restart: always
    logging:
      options:
        max-size: "10m"
        max-file: "10"

mongo db image          

In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/auth-service.yml
spring:
  data:
    mongodb:
      host: statistics-mongodb
      username: user
      password: ${MONGODB_PASSWORD}
      database: piggymetrics
      port: 27017

plain text credentials for auth mongo db

unencrypted communication (no sign of SSL use)

'''
datapoint_repo = CClass(component, "Datapoint Repository", stereotype_instances=[mongo_db])

add_links({statistics_service: datapoint_repo},
          role_name="target",
          stereotype_instances=[database_connector, authentication_with_plaintext_credentials,
                                authentication_scope_all_requests,
                                connector_code_plaintext_sensitive_data, unencrypted_communication])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/statistics-service.yml

security:
  oauth2:
    client:
      clientId: statistics-service
      clientSecret: ${STATISTICS_SERVICE_PASSWORD}
      accessTokenUri: http://auth-service:5000/uaa/oauth/token
      grant-type: client_credentials
      scope: server

authentication of oauth service uses plain text credentials, sensitive data in the code.


'''

add_links({statistics_service: oauth2},
          role_name="target",
          stereotype_instances=[auth_provider, restful_http, http, authentication_with_plaintext_credentials,
                                authentication_scope_all_requests, connector_code_plaintext_sensitive_data])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/account-service/src/main/java/com/piggymetrics/account/service/AccountServiceImpl.java

feign clients are autowired:

	@Autowired
	private StatisticsServiceClient statisticsClient;

	@Autowired
	private AuthServiceClient authClient;

	@Autowired
	private AccountRepository repository;

and then used

...
authClient.createUser(user);
...
statisticsClient.updateStatistics(name, account);   

In: https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/account-service.yml

feign:
  hystrix:
    enabled: true   

Services use customer tokens for authentication/authorization, like:
https://github.com/sqshq/piggymetrics/blob/master/statistics-service/src/main/java/com/piggymetrics/statistics/service/security/CustomUserInfoTokenServices.java

In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/account-service.yml
auth service is linked via plaintext credentials:
  oauth2:
    client:
      clientId: account-service
      clientSecret: ${ACCOUNT_SERVICE_PASSWORD}
      accessTokenUri: http://auth-service:5000/uaa/oauth/token
      grant-type: client_credentials
      scope: server

'''

add_links({account_service: statistics_service},
          role_name="target",
          stereotype_instances=[restful_http, http, secure_authentication_token, authentication_scope_all_requests,
                                token_based_authorization, authorization_scope_all_requests],
          label="Feign client")

# contains modelling from [*2]
add_links({account_service: oauth2},
          role_name="target",
          stereotype_instances=[auth_provider, restful_http, http, authentication_with_plaintext_credentials,
                                authentication_scope_all_requests, connector_code_plaintext_sensitive_data],
          label="Feign Client and OAuth2 Auth Provider")

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/notification-service/src/main/java/com/piggymetrics/notification/service/NotificationServiceImpl.java
    
feign clients are autowired:

	@Autowired
	private AccountServiceClient client;

and then used

String attachment = client.getAccount(recipient.getAccountName()); 

In:
https://github.com/sqshq/piggymetrics/blob/master/notification-service/src/main/java/com/piggymetrics/notification/client/AccountServiceClient.java
client impl

Services use customer tokens for authentication/authorization, like:
https://github.com/sqshq/piggymetrics/blob/master/account-service/src/main/java/com/piggymetrics/account/service/security/CustomUserInfoTokenServices.java

'''

add_links({notification_service: account_service},
          role_name="target",
          stereotype_instances=[restful_http, http, secure_authentication_token, authentication_scope_all_requests,
                                token_based_authorization, authorization_scope_all_requests],
          label="Feign client")

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/statistics-service/src/main/java/com/piggymetrics/statistics/service/ExchangeRatesServiceImpl.java

exchange rates client autowired and used:

@Autowired
	private ExchangeRatesClient client;

client.getRates(Currency.getBase());

used in statistics service:
https://github.com/sqshq/piggymetrics/blob/master/statistics-service/src/main/java/com/piggymetrics/statistics/service/StatisticsServiceImpl.java

@Autowired
	private ExchangeRatesService ratesService;

In:
https://github.com/sqshq/piggymetrics/blob/master/statistics-service/src/main/java/com/piggymetrics/statistics/client/ExchangeRatesClient.java
calls URL:
@FeignClient(url = "${rates.url}", name = "rates-client", fallback = ExchangeRatesClientFallback.class)
public interface ExchangeRatesClient {

    @RequestMapping(method = RequestMethod.GET, value = "/latest")
    ExchangeRatesContainer getRates(@RequestParam("base") Currency base);

}

Defined here:

https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/statistics-service.yml

rates:
  url: https://api.exchangeratesapi.io

uses https, but no authentication or authorization; external service
'''

exchange_rates_service = CClass(component, "Exchange Rate Service", stereotype_instances=[service, external_component])

add_links({statistics_service: exchange_rates_service},
          role_name="target",
          stereotype_instances=[restful_http, https],
          label="Feign client")

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/turbine-stream-service/src/main/java/com/piggymetrics/turbine/TurbineStreamServiceApplication.java
- Turbine Stream Service is enabled
- linked to eureka service

@SpringBootApplication
@EnableTurbineStream
@EnableDiscoveryClient
public class TurbineStreamServiceApplication 

In:
https://github.com/sqshq/piggymetrics/blob/master/docker-compose.yml
turbine image is used:

  turbine-stream-service:
    environment:
      CONFIG_SERVICE_PASSWORD: $CONFIG_SERVICE_PASSWORD
    image: sqshq/piggymetrics-turbine-stream-service
    restart: always
    depends_on:
      config:
        condition: service_healthy
    ports:
    - 8989:8989
    logging:
      options:
        max-size: "10m"
        max-file: "10"

In:
https://github.com/sqshq/piggymetrics/blob/master/turbine-stream-service/src/main/resources/bootstrap.yml

config service linked:

spring:
  application:
    name: turbine-stream-service
  cloud:
    config:
      uri: http://config:8888
      fail-fast: true
      password: ${CONFIG_SERVICE_PASSWORD}
      username: user

sensitive data (password) as plaintext 

In:
https://github.com/sqshq/piggymetrics/blob/master/turbine-stream-service/pom.xml

Dependencies to turbine stream and rabbit:

		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-netflix-turbine-stream</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-stream-rabbit</artifactId>
		</dependency>


In 
https://github.com/sqshq/piggymetrics/blob/master/docker-compose.yml

Rabbit MQ config:

  rabbitmq:
    image: rabbitmq:3-management
    restart: always
    ports:
      - 15672:15672
    logging:
      options:
        max-size: "10m"
        max-file: "10"

https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/application.yml

Rabbit MQ config:

spring:
  rabbitmq:
    host: rabbitmq

'''

turbine_stream_service = CClass(component, "Turbine Service Service", stereotype_instances=[monitoring_component])
add_links({turbine_stream_service: config},
          role_name="target", stereotype_instances=[restful_http, http, authentication_with_plaintext_credentials,
                                                    authentication_scope_all_requests,
                                                    connector_code_plaintext_sensitive_data])

'''
In:
https://github.com/sqshq/piggymetrics

In this project configuration, each microservice with Hystrix on board pushes metrics to Turbine via Spring Cloud Bus (with AMQP broker). The Monitoring project is just a small Spring boot application with Turbine and Hystrix Dashboard.

In:
https://github.com/sqshq/piggymetrics/blob/master/account-service/pom.xml

Hystrix dependencies:

		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
		</dependency>
		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-netflix-hystrix-stream</artifactId>
		</dependency>

In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/account-service.yml

Hystrix config for Feign on Account:

feign:
  hystrix:
    enabled: true



In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/application.yml

Hystrix config:

hystrix:
  command:
    default:
      execution:
        isolation:
          thread:
            timeoutInMilliseconds: 10000

In:
https://github.com/sqshq/piggymetrics/blob/master/config/src/main/resources/shared/gateway.yml

Hystrix config:

hystrix:
  command:
    default:
      execution:
        isolation:
          thread:
            timeoutInMilliseconds: 20000


In:
https://github.com/sqshq/piggymetrics/blob/master/statistics-service/pom.xml

Hystrix dependencies:

		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-netflix-hystrix-stream</artifactId>
		</dependency>

In:
https://github.com/sqshq/piggymetrics/blob/master/statistics-service/pom.xml

Hystrix dependencies:
	    <dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-netflix-hystrix-stream</artifactId>
		</dependency>

'''

add_links({account_service: turbine_stream_service},
          role_name="target", stereotype_instances=[messaging], label="Rabbit MQ Hystrix Stream")
add_links({statistics_service: turbine_stream_service},
          role_name="target", stereotype_instances=[messaging], label="Rabbit MQ Hystrix Stream")
add_links({notification_service: turbine_stream_service},
          role_name="target", stereotype_instances=[messaging], label="Rabbit MQ Hystrix Stream")

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/monitoring/src/main/java/com/piggymetrics/monitoring/MonitoringApplication.java
- monitoring application and hystrix dashboard enabled


@SpringBootApplication
@EnableHystrixDashboard
public class MonitoringApplication {

	public static void main(String[] args) {
		SpringApplication.run(MonitoringApplication.class, args);
	}
}

In: 
https://github.com/sqshq/piggymetrics/blob/master/monitoring/src/main/resources/bootstrap.yml

- linked to config service
spring:
  application:
    name: monitoring
  cloud:
    config:
      uri: http://config:8888
      fail-fast: true
      password: ${CONFIG_SERVICE_PASSWORD}
      username: use

sensitive data (password) as plaintext 

In:
https://github.com/sqshq/piggymetrics/blob/master/monitoring/pom.xml

Hystrix dashboard dependency:

		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-netflix-hystrix-dashboard</artifactId>
		</dependency>   

'''

hystrix_dashboard = CClass(component, "Monitoring App / Hystrix Dashboard",
                           stereotype_instances=[monitoring_dashboard])
add_links({hystrix_dashboard: config},
          role_name="target", stereotype_instances=[restful_http, http, authentication_with_plaintext_credentials,
                                                    authentication_scope_all_requests,
                                                    connector_code_plaintext_sensitive_data])

add_links({turbine_stream_service: hystrix_dashboard},
          role_name="target", stereotype_instances=[messaging], label="Rabbit MQ Hystrix Stream")

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/registry/src/main/java/com/piggymetrics/registry/RegistryApplication.java
@SpringBootApplication
@EnableEurekaServer
public class RegistryApplication {

	public static void main(String[] args) {
		SpringApplication.run(RegistryApplication.class, args);
	}
}

In:
https://github.com/sqshq/piggymetrics/blob/master/registry/src/main/resources/bootstrap.yml

link to config service:

  cloud:
    config:
      uri: http://config:8888
      fail-fast: true
      password: ${CONFIG_SERVICE_PASSWORD}
      username: user

eureka config:
eureka:
  instance:
    prefer-ip-address: true
  client:
    registerWithEureka: false
    fetchRegistry: false
    server:
      waitTimeInMsWhenSyncEmpty: 0

sensitive data (password) as plaintext 

'''

eureka_registry = CClass(component, "Eureka Registry Service", stereotype_instances=discovery_service)

add_links({eureka_registry: config},
          role_name="target", stereotype_instances=[restful_http, http, authentication_with_plaintext_credentials,
                                                    authentication_scope_all_requests,
                                                    connector_code_plaintext_sensitive_data])

'''
In:
https://github.com/sqshq/piggymetrics/blob/master/gateway/src/main/java/com/piggymetrics/gateway/GatewayApplication.java
https://github.com/sqshq/piggymetrics/blob/master/turbine-stream-service/src/main/java/com/piggymetrics/turbine/TurbineStreamServiceApplication.java
https://github.com/sqshq/piggymetrics/blob/master/auth-service/src/main/java/com/piggymetrics/auth/AuthApplication.java
https://github.com/sqshq/piggymetrics/blob/master/account-service/src/main/java/com/piggymetrics/account/AccountApplication.java
https://github.com/sqshq/piggymetrics/blob/master/notification-service/src/main/java/com/piggymetrics/notification/NotificationServiceApplication.java
https://github.com/sqshq/piggymetrics/blob/master/statistics-service/src/main/java/com/piggymetrics/statistics/StatisticsApplication.java
https://github.com/sqshq/piggymetrics/blob/master/turbine-stream-service/src/main/java/com/piggymetrics/turbine/TurbineStreamServiceApplication.java

we find @EnableDiscoveryClient -> eureka clients

no authentication could be found

'''

for c in [gateway, oauth2, account_service, notification_service, statistics_service, turbine_stream_service]:
    add_links({c: eureka_registry},
              role_name="target",
              stereotype_instances=[restful_http, http, no_authentication, authentication_scope_all_requests],
              label="Discovery Client")

'''
distributed tracing through Sleuth enabled in POM files, like:

<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-sleuth</artifactId>
			
in:
https://github.com/sqshq/piggymetrics/blob/master/auth-service/pom.xml
https://github.com/sqshq/piggymetrics/blob/master/statistics-service/pom.xml
https://github.com/sqshq/piggymetrics/blob/master/notification-service/pom.xml
https://github.com/sqshq/piggymetrics/blob/master/account-service/pom.xml
https://github.com/sqshq/piggymetrics/blob/master/gateway/pom.xml

Specific distributed tracing component used is not defined -> protocol/authentication of link undefined.


'''

sleuth_tracing = CClass(component, "Spring Cloud Sleuth / Slf4J MDC Based Tracing Component",
                        stereotype_instances=tracing_component)

for c in [gateway, statistics_service, account_service, notification_service, oauth2]:
    add_links({c: sleuth_tracing},
              role_name="target")

piggy_metrics = CBundle("piggy_metrics_all", elements=service_client.class_object.get_connected_elements())
piggy_metrics_services = CBundle("piggy_metrics_services", elements=[
    o.class_object for o in [service_client, gateway, notification_service, recipient_repo, account_service,
                             account_repo, statistics_service, exchange_rates_service, datapoint_repo]])

piggy_metrics_config = CBundle("piggy_metrics_config", elements=[
    o.class_object for o in [config, account_service, notification_service,
                             hystrix_dashboard, turbine_stream_service, statistics_service, eureka_registry,
                             gateway]])

piggy_metrics_monitoring_tracing_oauth = CBundle("piggy_metrics_monitoring_tracing_oauth", elements=[
    o.class_object for o in [hystrix_dashboard, turbine_stream_service, account_service, statistics_service,
                             notification_service, eureka_registry, oauth2, gateway, sleuth_tracing, user_repo]])

piggy_metrics.abbreviation = "PM0"
piggy_metrics.description = \
    "Piggy Metrics, a microservice system for demonstrating collecting application metrics in " + \
    "a microservice architecture using a Zuul API Gateway, OAuth2, Sleuth tracing, Histrix monitoring, a Eureka " + \
    "registry, and various per-service DBs. Source: \\url{https://github.com/sqshq/piggymetrics}."

piggy_metrics_views = [
    piggy_metrics, {},
    piggy_metrics_services, {},
    piggy_metrics_config, {},
    piggy_metrics_monitoring_tracing_oauth, {},

]

'''



TODO:   https://github.com/sqshq/piggymetrics/tree/master/gateway/src/main/resources/static
static pages on API gateway -> client impl  



'''
