pre_defined_intents = [{
                "tag": "noanswer",
                "patterns": [],
                "responses": ["Sorry, can't understand you", "Please give me more info", "Not sure I understand"],
                "context": [""]
            }, {
                "tag": "greeting",
                "patterns": ["Hi", "Hello", "Hey", "Hii", "there"],
                "responses": ["Hello, how can I help?", "Good to see you, how can I help you?", "Hi there, how can I help?"],
                "context": [""]
            },

            {
                "tag": "goodbye",
                "patterns": ["Bye", "See you later", "Goodbye", "Close", "Nice chatting to you, bye", "Till next time"],
                "responses": ["See you!", "Have a nice day", "Bye! Come back again soon."],
                "context": [""]
            },
            {
                "tag": "thanks",
                "patterns": ["Thanks", "Thank you", "Awesome, thanks", "Wow", "Amazing", "Great", "Good", "Nice", "Brilliant"],
                "responses": ["Happy to help!", "Any time!", "My pleasure"],
                "context": [""]
            },
            {
                "tag": "zzunknow_query",
                "patterns": ["boo", "much time"],
                "responses": ["Sorry, I'm not able to understand your question. Can you please ask a different question?"],
                "context": [""]
            },
            {
                "tag": "human",
                "patterns": ["person", "human", "agent", "representator", "man"],
                "responses": ["Sorry, No human representatives are avaialble right now. You can ask me instead"],
                "context": [""]
            }, {
                "tag": "ok",
                "patterns": ["ok", "okay", "fine", "right", "yes", "agreed"],
                "responses": ["Hope, I helped", "Good to know you are satisfied with my services", "Sure"],
                "context": [""]
            }
]