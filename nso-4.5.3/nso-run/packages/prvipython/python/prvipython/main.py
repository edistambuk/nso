# -*- mode: python; python-indent: 4 -*-

import ncs
from ncs.application import Service

#ova funkcija resetira vrijednosti jer prilikom novog upisivanja
#neke varijable mogu imati vrijednosti od proslog puta
#zasto nismo postavili vrijednost index-a na prazno? zato jer je on key

def init_vars(vars, key):
    ''' inicijalizira varijable '''
    if key == "rules":
        for i in ["SOURCE"]:
            vars.add(i, "")

def is_not_empty(nesto):
     if nesto is None:
        return False
     return True
# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):
    '''gfzju'''
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        ''' hjvfjk'''
        #ova naredba se locira na pocetak config-a
        self.log.info('Service create(service=', service._path, ')')

        #dohvaca template
        template = ncs.template.Template(service)

        #stvara biblioteku varijabli u koju ce upisat
        vars = ncs.template.Variables()

        #postavljam vrijednosti na te varijable
        vars.add("NAME", service.device)

        for single_chain in service.chain:
            vars.add("WHERE", single_chain.chain)

            #ovo smo napravili zato jer je tesko se referencirat service.rule.index
            for single_rule in single_chain.rule:
                #inicijaliziranje varijabli
                init_vars(vars, "rules")
                vars.add("INDEX", single_rule.index)

                #problem ako on nije ponuden
                #samo primjer ako nije mandatory ili key
                #ovaj je mandatory
                if(is_not_empty(single_rule.protocol)):
                    vars.add("PROTOCOL", single_rule.protocol)
                else:
                    vars.add("PROTOCOL", "")

                vars.add("SOURCE", single_rule.source)

                vars.add("DESTINATION", single_rule.destination)
                if single_chain.chain=='INPUT':
                    vars.add("INTERFACE_IN", single_rule.in_interface)
                    vars.add("INTERFACE_OUT", "")

                elif single_chain.chain=='OUTPUT':
                     vars.add("INTERFACE_IN", "")
                     vars.add("INTERFACE_OUT", single_rule.out_interface)
                else:
                     vars.add("INTERFACE_IN", single_rule.in_interface)
                     vars.add("INTERFACE_OUT", single_rule.out_interface)

                vars.add("JUMP", single_rule.jump)

                #treba primjenjivat nakon svake promjene
                #ako promjenis nesto vise puta te zatim primjenis ostaje samo zadnja vrijednost
                template.apply("prvipython", vars)

            template.apply("prvipython", vars)

        template.apply("prvipython", vars)


    # @Service.pre_lock_create
    # def cb_pre_lock_create(self, tctx, root, service, proplist):
    #     self.log.info('Service plcreate(service=', service._path, ')')

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    '''jhvhjik '''
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('prvipython', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
