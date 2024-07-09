from pydantic import BaseModel
from models.athlete import Gender


class SocialMedia(BaseModel):
    twitter: str = None
    instagram: str = None
    facebook: str = None

    def to_json(self):
        return {
            "twitter": self.twitter,
            "instagram": self.instagram,
            "facebook": self.facebook
        }

    @staticmethod
    def dict_to_social_media(response):
        return SocialMedia(twitter=response['twitter'] if response['twitter'] else "",
                           instagram=response['instagram'] if response['instagram'] else "",
                           facebook=response['facebook'] if response['facebook'] else "")


class Story(BaseModel):
    name: str = None
    date_of_birth: str = None
    place_of_birth: str = None
    social_media: SocialMedia
    biography: str = None
    childhood: str = None
    professional_career: str = None

    def to_json(self):
        return {
            "date_of_birth": self.date_of_birth,
            "place_of_birth": self.place_of_birth,
            "social_media": self.social_media.to_json(),
            "biography": self.biography,
            "childhood": self.childhood,
            "professional_career": self.professional_career
        }

    @staticmethod
    def dict_to_story(response):
        response['social_media'] = SocialMedia.dict_to_social_media(response['social_media'])
        return Story(**response)


class News(BaseModel):
    title: str
    banner_url: str
    redirection_url: str
    sportTag: str

    def to_json(self):
        return {
            "title": self.title,
            "banner_url": self.banner_url,
            "redirection_url": self.redirection_url,
            "sportTag": self.sportTag
        }


class AthleteDetail(BaseModel):
    id: int
    deeplink_to_share: str = None
    country: str = None
    flag: str = None
    sport: str = None
    gender: Gender = None
    profile_image_url: str = None
    detail: dict = {}
    story: Story = None
    news: list[News] = []

    def to_json(self):
        return {
            "id": self.id,
            "deeplink_to_share": self.deeplink_to_share,
            "country": self.country,
            "flag": self.flag,
            "sport": self.sport,
            "gender": self.gender,
            "profile_image_url": self.profile_image_url,
            "detail": self.detail,
            "story": self.story.to_json(),
            "news": [n.to_json() for n in self.news]
        }




# Create a json response of the following format for player - Neeraj Chopra
#
# // Urls for social media handle -- None, if not exists
# class SocialMedia:
#     twitter: str
#     instagram: str
#     facebook: str
#
# // biography , childhood and professional_carrers are 200-250 words descriptions
# class Story:
#     date_of_birth: str
#     place_of_birth: str
#     social_media: SocialMedia
#     biography: str
#     childhood: str
#     professional_career: str