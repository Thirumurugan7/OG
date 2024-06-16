import requests
import json

def test_generate_solidity_code():
    # Define the URL for the view
    url = 'http://localhost:8000/generate_solidity_code'  # Update with your actual URL

    # Define the data to be sent in the POST request
    data = {
        'text_data': '''
        a=10
        b=20
        c=a+b
        ''',
        'selected_language': 'solidity'
    }

    # Send a POST request to the view
    response = requests.post(url, data=data)

    # Ensure the response is successful (status code 200)
    if response.status_code == 200:
        response_data = response.json()
        print(response_data)

        # Check that 'solidity_code' and 'explain' keys are in the response
        if 'solidity_code' in response_data and 'explain' in response_data:
            print("Test passed!")
            print("Solidity Code:", response_data['solidity_code'])
            print("Explanation:", response_data['explain'])
        else:
            print("Test failed: 'solidity_code' or 'explain' not found in response.")
    else:
        print(f"Test failed: Received status code {response.status_code}")

# Run the test
test_generate_solidity_code()
