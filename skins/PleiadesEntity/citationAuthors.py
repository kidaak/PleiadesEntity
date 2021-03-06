## Script (Python) "citationAuthors"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

from Products.CMFCore.utils import getToolByName

mtool = getToolByName(context, 'portal_membership')

def userInByline(username):
    if username == 'T. Elliott': un = 'thomase'
    elif username == 'S. Gillies': un = 'sgillies'
    else: un = username
    member = mtool.getMemberById(un)
    if member:
        return {"id": member.getId(), "fullname": member.getProperty('fullname')}
    else:
        return {"id": None, "fullname": un}

def abbrev(a):
    parts = [p.strip() for p in a['fullname'].split(" ", 1)]
    if len(parts) == 2 and len(parts[0]) > 2:
        parts[0] = parts[0][0] + "."
    return " ".join(parts)

creators = list(context.Creators())
contributors = list(context.Contributors())
if "sgillies" in creators and ("sgillies" in contributors or "S. Gillies" in contributors):
    creators.remove("sgillies")
authors = [userInByline(name) for name in (creators + contributors)]

authors[1:] = map(abbrev, authors[1:])

parts = [p.strip() for p in authors[0]['fullname'].split(" ", 1)]
if len(parts) == 2 and len(parts[0]) > 2:
     parts[0] = parts[0][0] + "."
authors[0] = ", ".join(parts[::-1]) #last + ", " + first

return ", ".join(authors)

