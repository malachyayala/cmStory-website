import os
import random
from openai import OpenAI
from django.conf import settings

def get_random_item(file_path):
    with open(file_path, 'r') as f:
        return random.choice(f.readlines()).strip()
    
def generate_club_history_prompt(randomClub: str) -> str:
    return f"""
    I'm doing a FIFA career mode trying to generate important information to make my career mode more immersive and I need you to as a fifa career mode expert. 
    Make sure to pay close attention to the HTML tags I provide.
    Don't give me any extra text or output that is not asked for either, before or after the information requested.

    Here is an example of extra text that is not needed: Here’s the requested information about CA Osasuna in the specified HTML format:

    Please provie me with the following information about {randomClub} in an HTML format with the according tags.:
    <h4>Club Backstory:</h4>
    <p> Write an in-depth backstory of the club in a paragraph no longer than 10 sentences. Include at least 5 sentences about their 2 biggest rivals, and make it sound like a historian wrote it.</p>

    <h4>League History:</h4>
    <p> Write a paragraph about the history of the league {randomClub} is in. Focus on the 4 most successful clubs and the 5 biggest rivalries, explaining why they are rivals. Ensure it is no less than 6 sentences and sounds like a historian wrote it.</p>

    <h4>Club Philosophy:</h4>
    <p> Provide a 7-sentence paragraph about {randomClub}'s playing style and transfer philosophy.</p>

    <h4>Club Influence and Achievements:</h4>
    <p> Write a paragraph about {randomClub}'s influence on soccer. Include details about their most successful season in the league and continental competitions. Mention club legends and current key players, and make it sound like a historian wrote it.</p>
    """
    
def generate_club_background(club):
    client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
    
    response = client.chat.completions.create(
        model='your-model',
        messages=[{"role": "user", "content": generate_club_history_prompt(club)}],
        stream=False
    )
    final = response.choices[0].message.content
    noThinkResponse = final.split('</think>')[-1].strip()
    noHTMLResponse = noThinkResponse.split('```html')[-1].strip()
    return noHTMLResponse.split('```')[0].strip()

def generate_all():
    data_dir = os.path.join(settings.BASE_DIR, 'cmGenerator/data')
    cmClub  = get_random_item(os.path.join(data_dir, 'fifaClubTeams.txt'))
    
    return {
        'club': cmClub,
        'formation': get_random_item(os.path.join(data_dir, 'fifaFormations.txt')),
        'challenge': get_random_item(os.path.join(data_dir, 'fifaChallenges.txt')),
        'background': generate_club_background(cmClub)
    }