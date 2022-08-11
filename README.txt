Welcome

Endpoints:
    - "/api/user" - [GET] get all users
    - "/api/user" - [POST, Body: name, iin, email, password] create user
    - "/api/user/<int:id>" - [GET] retrive user
    - "/api/user/<int:id>" - [PUT, Body: name] update user
    - "/api/user/<int:id>" - [DELETE] delete user
    
    - "/api/card" - [GET] get all cards
    - "/api/card" - [POST, Body: owner_id] create card
    - "/api/card/<int:id>" - [GET] retrive card
    - "/api/card/<int:id>" - [PUT, Body: name] update card
    - "/api/card/<int:id>" - [DELETE] delete card
    - "/api/card/<int:id>/block" - [GET] disactive card
    - "/api/card/change-card" - [POST] change user card

    - "/api/pay" - [GET] create transaction