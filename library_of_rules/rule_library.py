
functionality_stereotypes = ["administration_server",
                            "configuration_server",
                            "gateway",
                            "message_broker",
                            "service_discovery",
                            "search_engine",
                            "web_application",
                            "web_server",
                            "authorization_server",
                            "authentication_server",
                            "logging_server",
                            "metrics_server",
                            "monitoring_dashboard",
                            "monitoring_server",
                            "tracing_server"
                            ]

def rule_set(model):
    """Set of all 25 out-of-the-box rules
    """

    results = dict()
    for rule in [r01, r02, r03, r04, r05,
                r06, r07, r08, r09, r10,
                r11, r12, r13, r14, r15,
                r16, r17, r18, r19, r20,
                r21, r22, r23, r24, r25]:
        results[rule.__name__] = rule(model)

    return results



def r01(model):
    """There should be a single service as entry point.
    """

    return model.nodes.exactly_one_is("entrypoint")


def r02(model):
    """All entry points should have a circuit breaker.
    """

    return model.nodes.that_are("entrypoint").all_have("circuit_breaker")


def r03(model):
    """All entry points should have a load balancer.
    """

    return model.nodes.that_are("entrypoint").all_have("load_balancer")


def r04(model):
    """All entry points should perform authorization.
    """

    return model.nodes.that_are("entrypoint").all_have("authorization")


def r05(model):
    """All entry points should perform authentication.
    """

    return model.nodes.that_are("entrypoint").all_have("authentication")


def r06(model):
    """All connections between services should be authorized.
    """

    return model.edges.sender_is("internal").receiver_is("internal").all_are("authorized")


def r07(model):
    """All connections between services should be authenticated.
    """

    return model.edges.sender_is("internal").receiver_is("internal").all_are("authenticated")


def r08(model):
    """There should be a single authorization service.
    """

    return model.nodes.exactly_one_is("authorization_server")


def r09(model):
    """There should be a single authentication service.
    """

    return model.nodes.exactly_one_is("authentication_server")


def r10(model):
    """No service that performs authorization should perform any other business functionality.
    """

    return model.nodes.that_are("authorization_server").none_are([s for s in functionality_stereotypes if (s != "authorization_server" and s != "token_server")])


def r11(model):
    """No service that performs authentication should perform any other business functionality.
    """

    return model.nodes.that_are("authentication_server").none_are([s for s in functionality_stereotypes if s != "authentication_server"])


def r12(model):
    """There should be a service limiting the number of login attempts.
    """

    return model.nodes.at_least_one_has("login_attempts_regulation")


def r13(model):
    """All connections between a service and an external entity should be encrypted.
    """

    return model.edges.sender_is("service").receiver_is("external_entity").all_are("encrypted").AND(model.edges.sender_is("external_entity").receiver_is("service").all_are("encrypted"))


def r14(model):
    """All connections between two services should be encrypted.
    """

    return model.edges.sender_is("service").receiver_is("service").all_are("encrypted")


def r15(model):
    """All services should perform logging.
    """

    return model.nodes.that_are("service").all_have("local_logging")


def r16(model):
    """There should be a single central logging subsystem.
    """

    return model.nodes.exactly_one_is("logging_server")


def r17(model):
    """There should be a message broker.
    """

    return model.nodes.at_least_one_is("message_broker")


def r18(model):
    """All services that perform logging should be connected to a message broker.
    """

    return model.nodes.that_are("internal").that_have("local_logging").all_are_connected_to("message_broker")


def r19(model):
    """No service that performs logging should be connected to a central logging subsystem.
    """

    return model.nodes.that_have("local_logging").none_are_connected_to("logging_server")


def r20(model):
    """There should be a monitoring dashboard.
    """

    return model.nodes.at_least_one_is("monitoring_dashboard")


def r21(model):
    """All services should be connected to a monitoring dashboard.
    """

    return model.nodes.that_are("service").all_are_connected_to("monitoring_dashboard")


def r22(model):
    """All services should sanitize logs.
    """

    return model.nodes.that_are("service").all_have("log_sanitization")


def r23(model):
    """There should be a single service registry.
    """

    return model.nodes.exactly_one_is("service_discovery")


def r24(model):
    """All service registries should have validation checks for incoming requests.
    """

    return model.nodes.that_are("service_discovery").all_have("validate_registration")


def r25(model):
    """There should be a single central secret store.
    """

    return model.nodes.exactly_one_is("secret_manager")


def r26(model):
    """For DeltAICert validation.
    """

    return model.edges.receiver_is("external_component").all_have("https").AND(model.edges.sender_is("external_component").all_have("https"))



#
