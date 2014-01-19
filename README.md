simpleGossip by Sean Reed
=========================


A Gossiping daemon that namespaces messages, letters, out into different mailboxes. These namespaces allow for system specific messages to be seperate from business logic messages. For example there is always a _system_ mailbox, but it only handles letters that describe the gossiping itself. Another namespace could be called _people_ this namespace would contain messages that contain information about _people_ rather than _system_ information. This allows for varying differnt local services to use a single daemon as well as partition out the business logic out into seperate mailboxes allow for a more organized approach.

JSON Format
===========

All messages are to be sent in the following format:

Requests:
```javascript
{ 
  'sender': String,      //Who sent the message
  'ttl': Integer,        //The TTL of the letter, a -1 means that it should continue to be propagated, 
                         //a value above this allows for partitioning the receiving set of nodes.
  'timestamp': Integer,  //When was this message sent.
  'letter': Object       //Object that contains the business logic specific data.
}
```

Letter definition:
```javascript
{
  'action': String,      //What should be done, or how is this data best described?
  'body': Object         //Business logic specific.
}
```

Response:
```javascript
{
  'status': Integer      //HTTP response code
  'body': Object         //Object that response the state, if there is one, of the current status, 
                         //business logic specific.
}
```

RESTful Interface
=================

Get gossiping information:
```bash
curl -X GET http://localhost -H "Content-Type: application/json"
```

```javascript
{ 
  'status': 200, 
  'body': 
  { 
    'fanout': 10, 
    'total_nodes': 5, 
    'total_letters_sent': 100, 
    'total_letters_received': 100, 
    'total_healthy_nodes': 3, 
    'total_unhealthy_nodes': 2, 
    'view': 
    [ 
      '192.168.1.1', 
      '192.168.1.2', 
      '192.168.1.6', 
      '192.168.1.8', 
      '192.168.1.10' 
    ], 
    'mailboxes': 
    [ 
      { 
        'name': 'system', 
        'mailbox_size': 100, 
        'mailbox_queue': 10 
      } 
    ] 
  } 
}
```

Setup a new mailbox:
```bash
curl -X GET http://localhost/mailbox -H "Content-Type: application/json" \
-d "{ 'sender': '127.0.0.1', 'ttl': -1, 'letter': { 'action': 'new_mailbox', 'body': { 'name': 'ants', 'size': 100 } } }"
```

```javascript
{ 
  'status': 200, 
  'body': {} 
}
```

List all the current mailboxes:
```bash
curl -X GET http://localhost/mailbox -H "Content-Type: application/json"
```

```javascript
{ 
  'status': 200, 
  'body': 
  { 
    'mailboxes': 
    [ 
      { 
        'name': 'ants', 
        'uri': 'http://localhost/mailbox/ants', 
        'total_messages': 2
      },
      ... 
    ] 
  } 
}
```

Retreive mailbox:
```bash
curl -X GET http://localhost/mailbox/ants -H "Content-Type: application/json"
```

```javascript
{ 
  'status': 200, 
  'body': 
  { 
    'letters': 
    [ 
      { 
        'sender': '192.168.1.3', 
        'ttl': -1, 
        'timestamp': 123456789, 
        'letter': 
        { 
          'action': 'new_node', 
          'body': 
          { 
            'who': '192.168.1.3' 
          } 
        } 
      },
      { 
        'sender': '192.168.1.4', 
        'ttl': -1, 
        'timestamp': 123456789, 
        'letter': 
        { 
          'action': 'failed_nodes', 
          'body': 
          { 
            'who': 
            [ 
              '192.168.1.5', 
              '192.168.1.6' 
            ] 
          } 
        } 
      } 
    ] 
  } 
}
```

Send a letter:
```bash
curl -X POST http://localhost/mailbox/ants -H "Content-Type: application/json" \ 
-d "{'sender': '192.168.1.2', 'timestamp': 1234567890, 'ttl': 2,  'letter': { 'action': 'election', 'body': { 'who': '192.168.1.1' } } }"
```

```javascript
{ 
  'status': 200, 
  'body': {} 
}
```

Delete a mailbox:
```bash
curl -X DELETE http://localhost/mailbox/ants -H "Content-Type: application/json"
```

```javascript
{ 
  'status': 200, 
  'body': {} 
}
```
