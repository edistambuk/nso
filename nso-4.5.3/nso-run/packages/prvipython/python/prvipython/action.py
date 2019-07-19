from ncs.dp import Action
import ncs
import ncs.maapi
class ActionCallback(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, action_input, action_output):
        self.log.info('Action Class triggered...')

        user='cisco'
        if name == 'device-print':
            self.log.info('device processed...')
            #sta je ovaj kp
            self.device_print(user,kp,action_input,action_output)
        elif name == 'print_num_of_rules':
            self.log.info('device processed...')
            #sta je ovaj kp
            self.print_num(user,kp,action_input,action_output)
        elif name == 'BLABLA':
            self.log.info('device processed blabla...')
            #sta je ovaj kp
            self.print_num(user,kp,action_input,action_output)
    def device_print(self, user,kp, action_input,action_output):
        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, user, 'python'):
                with m.start_write_trans() as t:
                    service = ncs.maagic.get_node(t, kp)
                    root = ncs.maagic.get_root(t)

                    device = action_input.device
                    if device is None or device == "":
                        device = service.primary_vnf

                    action_output.device = device
    def print_num(self, user,kp, action_input,action_output):
        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, user, 'python'):
                with m.start_write_trans() as t:
                    service = ncs.maagic.get_node(t, kp)
                    root = ncs.maagic.get_root(t)

                    device = action_input.device
                    if device is None or device == "":
                        device = service.primary_vnf

                    action_output.num_of_devices = 3





class KickerAction(ncs.application.Application):
    def setup(self):
        self.register_action('kicker-action',ActionCallback)

    def teardown(self):
        self.log.info('kicker-action FINISHED')