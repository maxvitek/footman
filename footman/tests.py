from __future__ import absolute_import
from footman.settings import COMMAND_KEYWORD

test_voice_plugin = {
    'result':
        [
            {
                'alternative': [
                    {
                        'transcript': COMMAND_KEYWORD + ' ' + 'say this is a test'
                    }
                ]
            }
        ]
}

test_wolfram_alpha_plugin = {
    'result':
        [
            {
                'alternative': [
                    {
                        'transcript': COMMAND_KEYWORD + ' ' + 'what is the population of Texas'
                    }
                ]
            }
        ]
}

test_nest_get_temp = {
    'result':
        [
            {
                'alternative': [
                    {
                        'transcript': COMMAND_KEYWORD + ' ' + 'what is the indoor temperature'
                    }
                ]
            }
        ]
}

test_nest_get_hum = {
    'result':
        [
            {
                'alternative': [
                    {
                        'transcript': COMMAND_KEYWORD + ' ' + 'what is the indoor humidity'
                    }
                ]
            }
        ]
}

test_nest_get_cond = {
    'result':
        [
            {
                'alternative': [
                    {
                        'transcript': COMMAND_KEYWORD + ' ' + 'what are the indoor conditions'
                    }
                ]
            }
        ]
}

test_nest_set_temp = {
    'result':
        [
            {
                'alternative': [
                    {
                        'transcript': COMMAND_KEYWORD + ' ' + 'set the indoor temperature to 65 degrees'
                    }
                ]
            }
        ]
}

test_start_chat = {
    'result':
        [
            {
                'alternative': [
                    {
                        'transcript': COMMAND_KEYWORD + ' ' + "let's chat"
                    }
                ]
            }
        ]
}

test_start_robot = {
    'result':
        [
            {
                'alternative': [
                    {
                        'transcript': COMMAND_KEYWORD + ' ' + 'launch the black robot'
                    }
                ]
            }
        ]
}

test_stop_robot = {
    'result':
        [
            {
                'alternative': [
                    {
                        'transcript': COMMAND_KEYWORD + ' ' + 'dock the black robot'
                    }
                ]
            }
        ]
}

test_turn_on_brtv = {
    'result':
        [
            {
                'alternative': [
                    {
                        'transcript': COMMAND_KEYWORD + ' ' + 'turn on the bedroom tv'
                    }
                ]
            }
        ]
}

test_turn_off_brtv = {
    'result':
        [
            {
                'alternative': [
                    {
                        'transcript': COMMAND_KEYWORD + ' ' + 'turn off the bedroom tv'
                    }
                ]
            }
        ]
}