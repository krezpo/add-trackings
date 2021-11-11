import glob
import json
import sys
import yaml

ENCODING = "UTF-8"

def has_tracking(name, entering_custom_actions):

    for action in entering_custom_actions:
        if action["$title"] == name:
            return True

    return False

if __name__ == "__main__":

    with open("config.yml") as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.SafeLoader)

    if config == None:
        sys.exit(-1)

    chatbots = glob.glob("{}/*.json".format(config["source_folder"]))

    with open(config["trackings"], 'r', encoding=ENCODING) as data:
        trackings = json.load(data)

    for chatbot in chatbots:
        print(chatbot)

        with open(chatbot, 'r', encoding=ENCODING) as data:
            builder = json.load(data)
        
        for state in builder:
            if state == "onboarding":
                continue

            if "desk:" in state:
                continue

            entering_custom_actions = builder[state]["$enteringCustomActions"]

            for i in range(0, len(trackings['$enteringCustomActions'])):
                if not has_tracking(name = trackings['$enteringCustomActions'][i]['$title'], entering_custom_actions = entering_custom_actions):
                    entering_custom_actions.append(trackings['$enteringCustomActions'][i])

        chatbot_name = str(chatbot.split("/")[-1]).replace(".json", "")
        with open("{}/{}.json".format(config["destination_folder"], chatbot_name), "w+", encoding=ENCODING) as output:
            json.dump(builder, output, indent=4, ensure_ascii=False)