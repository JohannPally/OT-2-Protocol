from aiohttp import web # You can install aiohttp with pip
import json

async def update(request):
    """
    This function serves POST /update.

    The request should have a json body with a "step" key that at some point
    has the value "done-aspirating".

    It will return a json message with appropriate HTTP status.
    """
    try:
        body = await request.json()
    except json.JSONDecodeError:
        text = await body.text()
        print(f"Request was not json: {text}")
        return web.json_response(status=400, # Bad Request
                                 data={'error': 'bad-request'})
    if 'step' not in body:
        print(f"Body did not have a 'step' key")
        return web.json_response(status=400, # Bad Request
                                 data={'error': 'no-step'})
    if body['step'] == 'done-aspirating':
       # Here you might for instance check a balance
       # attached to the computer to validate apsiration
       print("Robot is done aspirating")
       return web.json_response(status=200, # OK
                                data={'done': True})

# Create and run the actual server application
app = web.Application()
# Install the update function to serve the /update endpoint for POST
app.router.add_post('/update', update)
# Run the application
web.run_app(app, # our application
            host='0.0.0.0', # listen on all network interfaces
                            # (change to 127.0.0.1 to listen only to
                            # requests from this computer for testing)
            port=80)        # the standard http port; may need to
                            # change to something else if another
                            # server is running