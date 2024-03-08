*** This is a Simple Chat Application ***


=> Requirement: Docker setup

** Start the app using : docker

=> Main Port : 8005

=> Documentation : http://localhost:8005/api/docs/


=> Websocket URL : 


1.  ws://localhost:8005/ws/chat/<receiver_id>/



        => Sample Websocket Payload : {
                                            "message": "Hi John,
                                            "chat_id" : 1 , (Optional) #This is the chat id for case where the user wants to update a message
                                        }


        => Sample Websocket Query Param :
                                        token : "dfdfdfdfdfdgddg" ( this is the access token gotten from login)
                                        user: 1





2.  ws://localhost:8005/ws/chat/read_status/  : To get the read receipt status
3.  



== For the Frontend React App : http://localhost:3000