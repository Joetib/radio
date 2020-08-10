from .models import SocialLink

def get_social_context(*args, **kwargs):
    facebook = SocialLink.objects.filter(site="F")
    Twitter = SocialLink.objects.filter(site="T")
    Whatsapp = SocialLink.objects.filter(site="W")
    Youtube = SocialLink.objects.filter(site="Y")
    LinkedIn = SocialLink.objects.filter(site="L")
    Instagram = SocialLink.objects.filter(site="I")
    return {
        'facebook': facebook.first() if facebook.exists() else None,
        'Whatsapp': Whatsapp.first() if Whatsapp.exists() else None,
        'Twitter': Twitter.first() if Twitter.exists() else None,
        'Instagram': Instagram.first() if Instagram.exists() else None,
        'LinkedIn': LinkedIn.first() if LinkedIn.exists() else None,
        'Youtube': Youtube.first() if Youtube.exists() else None,
    }

