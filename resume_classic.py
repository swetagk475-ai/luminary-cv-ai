from jinja2 import Environment, FileSystemLoader

def generate_classic(data):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('resume_classic.html')
    
    return template.render(
        name=data['name'] or "Your Name",
        email=data['email'] or "email@example.com",
        summary=data['summary'] or "Professional summary...",
        experience=data['exp'] or "Work history...",
        projects=data['projects'] or "Key projects...", 
        skills=data['skills'].split(',') if data['skills'] else [],
        education=data['edu'] or "Education details..." 
    )