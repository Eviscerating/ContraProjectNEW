import httpx
from contra import settings

async def get_access_token()->str:
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
        'Content-Type': 'application/json',
    }
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET_ID)
    data = {
        'grant_type': 'client_credentials'
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            settings.PAYPAL_AUTH_URL,
            auth = auth, 
            headers = headers,
            data = data,
        )
        resp.raise_for_status()
        
        resp_data = resp.json()
        return resp_data['access_token']
    
async def cancel_subscription(
    access_token: str,
    subscription_id: str,
    reason = 'No reason provided'
):
    url = f'{settings.PAYPAL_BILLING_SUBSCRIPTIONS_URL}/{subscription_id}/cancel'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    }
    cancel_data = {'reason': reason}
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers = headers, json = cancel_data)
        resp.raise_for_status()
        print(f'[+] {resp.status_code}')
         
         
async def update_subscription_plan(
    access_token: str,
    subscription_id: str,
    new_plan_id: str,
    return_url: str,
    cancel_url: str,
)->str:
    url = f'{settings.PAYPAL_BILLING_SUBSCRIPTIONS_URL}/{subscription_id}/revise'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
    }
    update_data = {
        'plan_id': new_plan_id,
        'application_context': {
            'return_url': return_url,
            'cancel_url': cancel_url,
            'user_action': 'SUBSCRIBE_NOW',
        }
    }
    approval_url = ''
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers= headers, json = update_data)
        resp.raise_for_status()
        print(f"[+] {resp.status_code}")
        
        resp_data = resp.json()
        for link_details in resp_data.get('links', []):
            if link_details['rel'] == 'approve':
                approval_url = link_details['href']
                break
            
    return approval_url

async def get_subscription_details(
    access_token: str,
    subscription_id: str
)-> dict:
    url = f'{settings.PAYPAL_BILLING_SUBSCRIPTIONS_URL}/{subscription_id}'
    headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers = headers)
        resp.raise_for_status()
        return resp.json()
       