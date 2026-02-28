from jinja2 import Environment, FileSystemLoader

def generate_professional(data):
    # Setup Jinja2 to load from /templates folder
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('resume_professional.html')
    
    # Process skills into a clean list
    skills_list = []
    if data.get('skills'):
        skills_list = [s.strip() for s in data['skills'].split(',') if s.strip()]
    
    return template.render(
        name=data.get('name') or "Your Name",
        email=data.get('email') or "email@example.com",
        summary=data.get('summary') or "Professional summary...",
        experience=data.get('exp') or "Work history...",
        projects=data.get('projects') or "Key projects...", 
        skills=skills_list,
        education=data.get('edu') or "Education details..." 
    )