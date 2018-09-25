# -*- coding: utf-8 -*-

#----------------------------------------
# Web API for Danbee.ai ChatBot Platform
#----------------------------------------

import requests
import json
import csv



class Danbee():
    def __init__(self, chatbot_id=0):
        self.chatbot_id = chatbot_id


    def print_kor(self, text):
        #print(json.dumps(text, indent=4, ensure_ascii=False))
        print(text)


    def event_api(self, event, user_key):
        data_send = {
            'chatbot_id': 'c54e4466-d26d-4966-af1f-ca4d087d0c4a',
            'parameters': event
        }
        data_header = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        event_url = "https://danbee.ai/chatflow/54ae138f-fa8f-404f-8975-8ac6a3c45c35/eventFlow.do"
        res = requests.post(event_url,
                            data=json.dumps(data_send),
                            headers=data_header)
        data_receive = res.json()

        message = data_receive['responseSet']['result']['result'][0]['message']  # <- danbee json 포맷 분석 결과
        print("----- Event API ------")
        print(message)
        print("  ")

        return data_receive

    # ----------------------------------------------------
    # Danbee.ai에서 대답 구함
    # ----------------------------------------------------
    def get_answer_danbee(self, text, user_key):
        # --------------------------------
        # Danbee 요청
        # --------------------------------
        data_send = {
            'chatbot_id': self.chatbot_id,      # 'c54e4466-d26d-4966-af1f-ca4d087d0c4a'
            'input_sentence': text
        }
        data_header = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        danbee_chatflow_url = 'https://danbee.ai/chatflow/engine.do'

        res = requests.post(danbee_chatflow_url,
                            data=json.dumps(data_send),
                            headers=data_header)
        # --------------------------------
        # 대답 처리
        # --------------------------------
        '''
        if res.resultStatus != requests.codes.ok:
            return ERROR_MESSAGE
        '''

        data_receive = res.json()

        message = data_receive['responseSet']['result']['result'][0]['message']


        #answer = data_receive['result']

        print("\n")
        #print(user_key, ": ", text)
        #print("      [receptionbot]", ": ", message)

        sentence = user_key + ": " + text
        self.print_kor(sentence)
        sentence = "      [receptionbot]: " + message
        self.print_kor(sentence)


        self.print_kor(data_receive)

        return data_receive



    # ----------------------------------------------------
    # Dialogflow에서 대답 구함
    # ----------------------------------------------------
    def get_answer_dialogflow(self, text, user_key):
        # --------------------------------
        # Dialogflow에 요청
        # --------------------------------
        data_send = {
            'lang': 'ko',
            'query': text,
            'sessionId': user_key,
            'timezone': 'Asia/Seoul'
        }

        data_header = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': 'Bearer 9d10041bdb9c4c68a88b7899ca1540c1'  # Dialogflow의 Client access token 입력
        }

        dialogflow_url = 'https://api.dialogflow.com/v1/query?v=20150910'


        print('test ---- ')

        res = requests.post(dialogflow_url,
                            data=json.dumps(data_send),
                            headers=data_header)

        # --------------------------------
        # 대답 처리
        # --------------------------------
        if res.status_code != requests.codes.ok:
            return ERROR_MESSAGE

        data_receive = res.json()
        answer = data_receive['result']


        #print(user_key, ": ", text)
        #print("      [receptionbot]", ": ", answer)
        self.print_kor(user_key + ": " + text)
        self.print_kor("      [receptionbot]: " + answer)


        return answer


    # ----------------------------------------------------
    # POST test to heroku for database
    # ----------------------------------------------------
    def test_post(self, name):
        # --------------------------------
        # 요청
        # --------------------------------
        data_send = {
            'name': name
        }

        data_header = {
            'Content-Type': 'application/json; charset=utf-8'
        }

        dialogflow_url = 'https://heroku-dialogflow-chatbot.herokuapp.com/message_danbee'


        res = requests.post(dialogflow_url,
                            data=json.dumps(data_send),
                            headers=data_header)

        # --------------------------------
        # 대답 처리
        # --------------------------------
        if res.status_code != requests.codes.ok:
            return ERROR_MESSAGE

        data_receive = res.json()

        #print(data_receive)

        print('----------  Test from heroku -----------')
        print(json.dumps(data_receive, indent=4, ensure_ascii=False))
        print('----------------------------------------')


    # ----------------------------------------------------
    # database from CSV file
    # ----------------------------------------------------
    def get_datatbase(self, kind_of_guide):
        filename = 'RMI_researchers.csv'

        with open(filename, 'r', encoding='UTF-8-sig') as f:
            csv_data = csv.reader(f, delimiter=',')
            print("-------------")
            dict = {}
            row_cnt = 0
            for row in csv_data:
                row_cnt = row_cnt + 1
                if row_cnt == 1:
                    key = row
                else:
                    for i in range(0, len(row), 1):
                        if i == 0:
                            # print(dict_name)
                            dict_info = {}
                        else:
                            dict_info.update({key[i]: row[i]})
                            # print(dict_info)
                    dict.update({row[0]: dict_info})
                    # print("dict_name = ", dict_name)

        #json_data = json.dumps(dict, indent=4, ensure_ascii=False)
        #print(json_data)


        return dict




def main():

    # --------------------------------
    # Start Chat with Danbee API
    # --------------------------------
    user_key = 'DeepTasK'
    chatbot_id = 'c54e4466-d26d-4966-af1f-ca4d087d0c4a'

    chat = Danbee(chatbot_id)

    content = '안녕하세요'
    res = chat.get_answer_danbee(content, user_key)
    message = res['responseSet']['result']['result'][0]['message']   # <- danbee json 포맷 분석 결과
    print(message)




#----------------------------------------------------
# 메인 함수
#----------------------------------------------------
if __name__ == '__main__':

    main()
