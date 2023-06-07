from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from ovos_utils.process_utils import RuntimeRequirements
from ovos_utils import classproperty
from api_scripts.bashhandler import SSHExecutor

class MyTestSkill(MycroftSkill):
    def __init__(self):
        """ The __init__ method is called when the Skill is first constructed.
        It is often used to declare variables or perform setup actions, however
        it cannot utilise MycroftSkill methods as the class does not yet exist.
        """
        super().__init__()
        self.learning = True
        self.executor = SSHExecutor('doraemon')

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(internet_before_load=False,
                                   network_before_load=False,
                                   gui_before_load=False,
                                   requires_internet=False,
                                   requires_network=False,
                                   requires_gui=False,
                                   no_internet_fallback=True,
                                   no_network_fallback=True,
                                   no_gui_fallback=True)

    def initialize(self):
        """ Perform any final setup needed for the skill here.
        This function is invoked after the skill is fully constructed and
        registered with the system. Intents will be registered and Skill
        settings will be available."""
        my_setting = self.settings.get('my_setting')

    @intent_handler(IntentBuilder('ThankYouIntent').require('ThankYouKeyword'))
    def handle_thank_you_intent(self, message):
        """ This is an Adapt intent handler, it is triggered by a keyword."""
        self.speak_dialog("welcome")

    @intent_handler('HowAreYou.intent')
    def handle_how_are_you_intent(self, message):
        """ This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        self.speak_dialog("how.are.you")
        self.log.info("Message parsed is " + str(message))
    
    @intent_handler('RunCommand.intent')
    def handle_how_are_you_intent(self, message):
        """ 
        everything else is a command
        """
        self.log.info("Message parsed is " + str(message))
        received_text = message.data.get('utterance')
        if not received_text:
            self.speak_dialog("invalid text")
            return
        # Establish the SSH session
        self.executor.connect()
        self.executor.run_commands(received_text)
        self.executor.close()
    
    @intent_handler(IntentBuilder('CurrentProfileIntent')
                    .require('Profilevocab'))
    def get_profile(self, message):
        """
        return the user's profile
        """
        self.log.info("Message3 parsed is " + str(message.__dict__))
        received_text = message.data.get('utterance')
        if not received_text:
            self.speak_dialog("invalid text")
            return
        # Get the current profile
        current_profile = self.executor.get_profile()
        self.speak_dialog("current profile is " + current_profile)

    @intent_handler(IntentBuilder('SwitchProfileIntent')
                    .require('Profilevocab'))
    def switch_profile(self, message):
        """
        Switch the user's profile
        """
        self.log.info("Message3 parsed is " + str(message.__dict__))
        received_text = message.data.get('utterance')
        if not received_text:
            self.speak_dialog("invalid text")
            return
        # Set a new profile
        self.executor.set_profile(received_text)

        self.speak_dialog("switched profile successfully")
        # Establish the SSH session
        # executor.connect()

        # # Run commands
        # executor.run_commands()

        # # Close the SSH session
        # executor.close()

    def stop(self):
        pass


def create_skill():
    return MyTestSkill()
