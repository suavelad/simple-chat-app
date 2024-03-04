*** This is a Simple Chat Application ***


=> Requirement: Docker setup

** Start the app using : docker

=> Main Port : 8005

==> Documentation : http://localhost:8005/api/docs/


==> Websocket URL : ws://localhost:8005/ws/chat/
==> Set Header with "token" : This token is gotten using the login api ( access_token )
==> Sample Websocket Payload : {
                                    "sender" : 1,
                                    "receiver" : 2,
                                    "message": "Hi John
                                }
    Sample Websocket Query Param :
            token : "dfdfdfdfdfdgddg"
            user: 1





