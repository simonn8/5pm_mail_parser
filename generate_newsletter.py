from jinja2 import Environment, FileSystemLoader

opening_text_1 = "In tonight's 5pm briefing, as the UK plunges into recession, Chancellor Jeremy Hunt is pushed to initiate tax cuts to revitalize the struggling economy, amidst predictions of a short-lived downturn and calls for pro-growth policies ahead of the March budget. In other news, former minister Robert Jenrick reveals small boat migrants posing a 'real harm' to Britons are under constant watch by security services, highlighting the national security risk amid ongoing debates on illegal migration. Meanwhile, supermodel Naomi Campbell unveils a germ-fighting travel clothing line with Boss, featuring anti-bacterial and anti-stress properties, amidst her well-known germophobia."
opening_text_2 = "Meanwhile, supermodel Naomi Campbell unveils a germ-fighting travel clothing line with Boss, featuring anti-bacterial and anti-stress properties, amidst her well-known germophobia."

environment = Environment(loader=FileSystemLoader("data/"))
template = environment.get_template("newsletter_5pm_240215.txt")

content = template.render(opening_text_1=opening_text_1, opening_text_2=opening_text_2)

print(f"... template rendered")

filename = "data/newsletter_5pm_240215_generated.html"
with open(filename, mode="w", encoding="utf-8") as message:
    message.write(content)
    print(f"... wrote {filename}")
