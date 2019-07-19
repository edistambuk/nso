from ncs.dp import Action
import ncs
import ncs.maapi


class MyKickerCallback(Action):

    @Action.action
    def cb_action(self, uinfo, name, kp, action_input, action_output):
        self.log.info('Action Class triggered...')

        # local nso user used in requests
        user = 'cisco'  #admin
        self.log.info('name is: ', name)
        if name == 'insert':
            self.log.info('insert-action triggered...')
            self.insert(user, kp, action_input, action_output)

    def insert(self, user, kp, action_input, action_output):
        self.log.info("i'm here 1")
        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, user, 'python'):
                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)

                    device = action_input.device
                    address = action_input.address
                    port = action_input.port
                    authgroup = action_input.authgroup

                    template = ncs.template.Template(root.drugipython__actions)
                    vars = ncs.template.Variables()

                    vars.add('DEVICE', device)
                    vars.add('ADDRESS', address)
                    vars.add('PORT', port)
                    vars.add('AUTHGROUP', authgroup)
                    self.log.info(authgroup)

                    template.apply('insert_device', vars)

                    host_keys_input = root.devices.device[device].ssh.fetch_host_keys.get_input()
                    output = root.devices.device[device].ssh.fetch_host_keys(host_keys_input)

                    #IF ERROR IN OUTPUT
                    # return

                    sync = root.devices.device[device].sync_from.get_input()
                    output2 = root.devices.device[device].sync_from(sync)

                    #IF ERROR IN OUTPUT2
                    # return
                    if output2.result:
                        action_output.result="true"
                        t.apply()
                    else:
                        action_output.result=output2.info


class KickerAction(ncs.application.Application):

    def setup(self):
        self.log.info('kicker-action STARTED')
        self.register_action('my-kicker-action', MyKickerCallback)

    def teardown(self):
        self.log.info('kicker-action FINISHED')
