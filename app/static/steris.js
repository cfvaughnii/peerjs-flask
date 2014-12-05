      var session = Object;
      var success = false;
      var publisher = Object;
      var subscriber = Object;
      var us_width = "264px";
      var us_height = "198px";
      var them_width = "640px";
      var them_height = "360px";
      var api_key = "";
      var session_id = "";
      var token = "";
      var nickname = "";
      var globalAudioLevel = 0;
      var publisherVideoState = true;
      var publisherAudioState = false;
      var voiceCallOnly = false;


      function initialize_session(name) {
        nickname = name;
        $.ajax({url: "/api",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"jsonrpc": "2.0",
                "method": "getSessionToken", "params": [], "id": "1",
            }),
            dataType: "json",
            success: function(response) {
                var session_token_arr = response.result;
                console.log("getSessionToken: " + session_token_arr);
                api_key = session_token_arr[0];
                session_id = session_token_arr[1];
                token = session_token_arr[2];
                session = OT.initSession(api_key, session_id);
                do_connect_session();
            },
        });      
      };
      /*
          Connect session using api_key, session_id, token
      */       
      function do_connect_session() {

        session.connect(token, function(error) {
          if (error) {
            alert(error);
            console.log(error);
          } else {


            if (session.capabilities.forceDisconnect == 1) {
              console.log(" The client can forceDisconnect. See the next section.");
            } else {
              console.log(" The client cannot moderate.");
            }

            if (session.capabilities.forceUnpublish == 1) {
              console.log(" The client can forceUnpublish.");
            } else {
              console.log("The client cannot moderate.");
            }
            session.on("streamCreated", function(event) {
              console.log("New stream in the session: " + event.stream.streamId);
              var subscriberProperties = {insertMode: "append"};
              subscriber = session.subscribe(event.stream, "OT_them_view", subscriberProperties, function (error) {
              if (error) {
                console.log(error);
              } else {
                var subscribeElement = document.getElementById(subscriber.id);
                subscribeElement.style.top = "0px";
                subscribeElement.style.left = "0px";
                subscribeElement.style.height = them_height;
                subscribeElement.style.width = them_width;
                //var ot_edge =$("[class*='OT_edge-bar-item']");
                //ot_edge.hide();
                console.log("Subscriber added.");
                }
              });
            });

            session.on("streamDestroyed", function(event) {
              //alert("streamDestroyed")
            });

            session.on("streamPropertyChanged", function (event) {
              var subscribers = session.getSubscribersForStream(event.stream);
              for (var i = 0; i < subscribers.length; i++) {
                var s = subscribers[i];
                console.log(s.guid + " " + event.changedProperty +  " hasVideo changed ");
              }
            });
            /*
            proximity information received from 'them'
            */       
            session.on("signal:proximity", function(event) {
             console.log("proximity " + event.data);
             //The GUI call goes here
            });
            /*
            Send the proximity information received from 'them' to the GUI element
            */       
            session.on("signal:ringingVideo", function(event) {
              voiceCallOnly = false;
              sent_token = $.parseJSON(event.data);
              if (sent_token.token != token) {
                console.log("ringing " + event.data);
                var options = {
                    "keyboard" : true,
                    "backdrop" : "static",
                    "show" : true

                }              
                caller_id = sent_token.caller_id;
                calling = sent_token.calling;
                if (calling == nickname) {
                  $('#basicModal').find('.modal-title').text('Call from ' + caller_id);
                  $('#basicModal').modal(options);              
                  $('#basicModal').show();              
                }
              }
            });
            /*
            Send the proximity information received from 'them' to the GUI element
            */       
            session.on("signal:ringingVoice", function(event) {
              voiceCallOnly = true;
              sent_token = $.parseJSON(event.data);
              caller_id = sent_token.caller_id
              if (sent_token.token != token) {
                console.log("ringing " + event.data);
              }
            });

            session.on("signal:hangupSubscriber", function(event) {
              $("#toggles").hide();
              $("#calls").show();
              console.log("hangupSubscriber " + event.data);
              hangupSubscriber();
            });

            session.on("signal:hangupPublisher", function(event) {
              $("#toggles").hide();
              $("#calls").show();
              console.log("hangupPublisher " + event.data);
              hangupPublisher();
            });

            session.on("signal:forceHangup", function(event) {
              console.log("forceHangup " + event.data);
              hangupCall();
            });

            session.on("signal:acceptedVideo", function(event) {
              $('#basicModal').hide();              
              $("#toggles").show();
              $("#calls").hide();
              sent_token = $.parseJSON(event.data);
              if (sent_token.token != token) {
                console.log("accepted " + event.data);
                startPublish();
              }
            });
            
            session.on("signal:acceptedAudio", function(event) {
              $('#basicModal').hide();              
              $("#toggles").show();
              $("#calls").hide();
              sent_token = $.parseJSON(event.data);
              if (sent_token.token != token) {
                console.log("accepted " + event.data);
                startPublish();
              }
            });
          }
       });
      }


      var hideAll = function() {
          $("#OT_us_view").hide();
          $("#OT_them_view").hide();
      }

      var showAll = function() {
          $("#OT_us_view").show();
          $("#OT_them_view").show();
      }
      
      var startPublish = function () {
        var targetElement = "OT_us_view";
        var pubOptions = { publishAudio:publisherAudioState, publishVideo:publisherVideoState };
         
        // Replace replacementElementId with the ID of the DOM element to replace:
        publisher = OT.initPublisher(targetElement, pubOptions, function(error) {
          if (error) {
            // The client cannot publish.
            // You may want to notify the user.
          } else {
            console.log('Publisher initialized.');
            //var pubElement = document.getElementById(publisher.id);
            //pubElement.style.top = "375px";
            //pubElement.style.left = " 360px";
            //pubElement.style.height = us_height;
            //pubElement.style.width = us_width;
            session.publish(publisher);
          }
        });
      }

      var stopPublish = function() { 
        session.unsubscribe(subscriber);
        session.unpublish(publisher);
      }

      /*
          Function to send a signal to all subscribers
      */       
      function send_message(signal_type, json_string) {
        console.log("send signal " + json_string);
        session.signal(
          {
            data:json_string,
            type:signal_type
          },
          function(error) {
            if (error) {
              console.log("signal error ("
                           + error.code
                           + "): " + error.reason);
            } else {
              console.log("signal sent.");
            }
          }
        );
      }

      var isVoiceCall = function() {
        return voiceCallOnly;
      }

      var isVideoCall = function() {
        return !voiceCallOnly;
      }

      var videoCall = function(caller_id, calling) { 
        voiceCallOnly = false;
        send_message("ringingVideo", JSON.stringify({"token":token, "caller_id":caller_id,"calling":calling}));
      }

      var voiceCall = function(caller_id) { 
        voiceCallOnly = true;
        publisherAudioState = true;
        send_message("ringingVoice", JSON.stringify({"token":token, "caller_id":caller_id}));
      }
      /*
        The acceptCall function is called
        Do the following:
          1) Turn on Connedted state
          2) Publish our side
          3) Show the OT_us_view
      */
      var acceptCall = function() { 
        $('#basicModal').hide();              
        $("#toggles").show();
        $("#calls").hide();

        startPublish();
        if (voiceCallOnly)
          send_message("acceptedAudio",JSON.stringify({"token":token}));
        else
          send_message("acceptedVideo",JSON.stringify({"token":token}));

      }


      var hangupSubscriber = function() { 
        session.unsubscribe(subscriber);
      }

      var hangupPublisher = function() { 
       session.unpublish(publisher);
      }

      var hangupCall = function() { 
        $("#toggles").hide();
        $("#calls").show();
        send_message("hangupSubscriber",JSON.stringify({"token":token}));
        send_message("hangupPublisher",JSON.stringify({"token":token}));
      }

      var videoOn = function() {
        publisherVideoState = true;
        publisher.publishVideo(publisherVideoState);
      };
      var audioOn = function() {
        publisherAudioState = true;
        publisher.publishAudio(publisherAudioState);
      };
      var videoOff = function() {
        publisherVideoState = false;
        publisher.publishVideo(publisherVideoState);
      };
      var audioOff = function() {
        publisherAudioState = false;
        publisher.publishAudio(publisherAudioState);
      };
      var videoToggle = function() {
        publisherVideoState = !publisherVideoState;
        publisher.publishVideo(publisherVideoState);
      };
      var audioToggle = function() {
        publisherAudioState = !publisherAudioState;
        publisher.publishAudio(publisherAudioState);
      };

