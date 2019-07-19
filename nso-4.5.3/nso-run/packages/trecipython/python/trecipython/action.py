from ncs.dp import Action
import ncs
import ncs.maapi


class ActionCallback(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, action_input, action_output):
        self.log.info('Action Class triggered...')

        # local nso user used in requests
        user = 'cisco'
        if name == 'sync-from':
            self.log.info('sync-key triggered...')
            self.sync_key(user, kp)

    def sync_key(self,user,kp):
        self.log.info('dosao sam u sync_key akciju')
        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, user, 'python'):
                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)
                    service = ncs.maagic.get_node(t, kp)

                    self.log.info('presao sam withove u sync_key akciji')
                    device = service.device

                    host_keys_input = root.devices.device[device].ssh.fetch_host_keys.get_input()
                    root.devices.device[device].ssh.fetch_host_keys(host_keys_input)

                    self.log.info('sync-from za ' + device)
                    sync = root.devices.device[device].sync_from.get_input()
                    out = root.devices.device[device].sync_from(sync)

                    if out.result:
                        self.log.info("true")
                    else:
                        self.log.info(out.info)



class KickerAction(ncs.application.Application):

    def setup(self):
        self.log.info('kicker-action STARTED')
        self.register_action('trecipython-actionpoint', ActionCallback)

    def teardown(self):
        self.log.info('kicker-action FINISHED')
