import requests
from uuid import uuid4

class Guilded:
	def __init__(self, platform: str = "native"):
		self.api = "https://www.guilded.gg/api"
		self.headers = {
			"user-agent": "okhttp/3.12.12",
			"content-type": "application/json"
		}
		self.user_id = None
		self.platform = platform
		self.hmac_signed_session = None

	def login(self, email: str, password: str):
		data = {
			"email": email,
			"password": password
		}
		response = requests.post(
			f"{self.api}/login",
			json=data,
			headers=self.headers)
		json = response.json()
		cookies = response.cookies
		if "user" in json:
			self.gk = cookies["gk"]
			self.user_id = json["user"]["id"]
			self.guilded_mid = cookies["guilded_mid"]
			self.guilded_ipah = cookies["guilded_ipah"]
			self.hmac_signed_session = cookies["hmac_signed_session"]
			self.headers["cookie"] = f"guilded_mid={self.guilded_mid}; guilded_ipah={self.guilded_ipah}; hmac_signed_session={self.hmac_signed_session}; authenticated=true gk={self.gk}"
		return json

	def register(
			self,
			nickname: str,
			email: str,
			password: str):
		data = {
			"extraInfo": {},
			"name": nickname,
			"email": email,
			"password": password,
			"fullName": nickname
		}
		return requests.post(
			f"{self.api}/users?type=email",
			json=data,
			headers=self.headers).json()

	def get_user_channels(self, user_id: str):
		return requests.get(
			f"{self.api}/users/{user_id}/channels",
			headers=self.headers).json()

	def get_user_posts(
			self,
			user_id: str,
			limit: int = 1,
			offset: int = 0):
		return requests.get(
			f"{self.api}/users/{user_id}/posts?maxPosts={limit}&offset={offset}",
			headers=self.headers).json()

	def get_user_profile(self, user_id: str):
		return requests.get(
			f"{self.api}/users/{user_id}/profilev3",
			headers=self.headers).json()

	def create_team(self, team_name: str):
		data = {
			"extraInfo": {
				"platform": self.platform
			},
			"userId": self.user_id,
			"teamName": team_name
		}
		return requests.post(
			f"{self.api}/teams",
			json=data,
			headers=self.headers).json()

	def get_current_user(
			self,
			is_login: bool = False,
			is_v2: bool = True):
		return requests.get(
			f"{self.api}/me?isLogin={is_login}&v2={is_v2}",
			headers=self.headers).json()

	def get_team_groups(self, team_id: str):
		return requests.get(
			f"{self.api}/teams/{team_id}/groups",
			headers=self.headers).json()

	def get_team_channels(self, team_id: str):
		return requests.get(
			f"{self.api}/teams/{team_id}/channels",
			headers=self.headers).json()

	def get_team_members(self, team_id: str):
		return requests.get(
			f"{self.api}/teams/{team_id}/members",
			headers=self.headers).json()

	def get_team_info(self, team_id: str):
		return requests.get(
			f"{self.api}/teams/{team_id}/info",
			headers=self.headers).json()

	def send_message(
			self,
			channel_id: str,
			message: str,
			is_confirmed: bool = False,
			is_silent: bool = False,
			is_private: bool = False):
		data = {
			"messageId": uuid4(),
			"content": {
				"object": "value",
				"document": {
					"object": "document",
					"data": {},
					"nodes": [
						{
							"object": "block",
							"type": "paragraph",
							"data": {},
							"nodes": [
								{
									"object": "text",
									"leaves": [
										{
											"object": "leaf",
											"text": message,
											"marks": []
										}
									]
								}
							]
						}
					]
				}
			},
			"repliesToIds": [],
			"confirmed": is_confirmed,
			"isSilent": is_silent,
			"isPrivate": is_private
		}
		return requests.post(
			f"{self.api}/channels/{channel_id}/messages",
			json=data,
			headers=self.headers).json()

	def explore_teams(
			self,
			limit: int = 10,
			sections: list = ["proTeams", "verifiedTeams", "popularTeams"]):
		data = {
			"limit": limit,
			"sections": sections
		}
		return requests.post(
			f"{self.api}/explore/teams",
			json=data,
			headers=self.headers).json()

	def email_verify(self):
		return requests.post(
			f"{self.api}/email/verify",
			headers=self.headers).json()

	def join_team(self, team_id: str):
		return requests.put(
			f"{self.api}/teams/{team_id}/members/{self.user_id}/join",
			headers=self.headers).json()

	def leave_team(self, team_id: str):
		return requests.delete(
			f"{self.api}/teams/{team_id}/members/{self.user_id}",
			headers=self.headers).json()

	def search_teams(self, query: str, limit: int = 20):
		return requests.get(
			f"{self.api}/search?query={query}&entityType=team&maxResultsPerType={limit}",
			headers=self.headers).json()

	def search_users(self, query: str, limit: int = 20):
		return requests.get(
			f"{self.api}/search?query={query}&entityType=user&maxResultsPerType={limit}&excludedEntityIds={self.user_id}",
			headers=self.headers).json()

	def change_activity_status(self, status: int):
		data = {"status": status}
		return requests.post(
			f"{self.api}/users/me/presence",
			json=data,
			headers=self.headers).json()

	def change_profile_status(
			self,
			status: str,
			custom_reaction_id: int):
		data = {
			"content": {
				"object": "value",
				"document": {
					"object": "document",
					"data": {},
					"nodes": [
						{
							"object": "block",
							"type": "paragraph",
							"data": {},
							"nodes": [
								{
									"object": "text",
									"leaves": [
										{
											"object": "leaf",
											"text": status,
											"marks": []
										}
									]
								}
							]
						}
					]
				}
			},
			"customReactionId": custom_reaction_id
		}
		return requests.post(
			f"{self.api}/users/me/status",
			json=data,
			headers=self.headers).json()

	def get_friends_list(self):
		return requests.get(
			f"{self.api}/users/me/friends",
			headers=self.headers).json()

	def send_friend_request(self, user_ids: list):
		data = {"friendUserIds": user_ids}
		return requests.post(
			f"{self.api}/users/me/friendrequests",
			json=data,
			headers=self.headers).json()

	def cancel_friend_request(self, user_id: str):
		data = {"friendUserId": user_id}
		return requests.delete(
			f"{self.api}/users/me/friendrequests",
			json=data,
			headers=self.headers).json()

	def start_dm(self, user_id: str):
		data = {
			"users": [
				{
					"id": user_id
				}
			]
		}
		return requests.post(
			f"{self.api}/users/{self.user_id}/channels",
			json=data,
			headers=self.headers).json()

	def get_channel_messages(self, channel_id: str, limit: int = 20):
		return requests.get(
			f"{self.api}/channels/{channel_id}/messages?limit={limit}",
			headers=self.headers).json()

	def block_user(self, user_id: str):
		return requests.post(
			f"{self.api}/users/{user_id}/block",
			headers=self.headers).json()

	def unblock_user(self, user_id: str):
		return requests.post(
			f"{self.api}/users/{user_id}/unblock",
			headers=self.headers).json()

	def edit_profile(
			self,
			tagline: str = None,
			bio: str = None):
		data = {
			"userId": self.user_id
		}
		if tagline:
			data["aboutInfo"] = {"tagLine": tagLine}
		if bio:
			data["aboutInfo"] = {"bio": bio}
		return requests.put(
			f"{self.api}/users/{self.user_id}/profilev2",
			json=data,
			headers=self.headers).json()

	def create_post(self, title: str, description: str):
		data = {
			"userId": self.user_id,
			"title": title,
			"message": {
				"object": "value",
				"document": {
					"object": "document",
					"data": {},
					"nodes": [
						{
							"object": "block",
							"type": "paragraph",
							"data": {},
							"nodes": [
								{
									"object": "text",
									"leaves": [
										{
											"object": "leaf",
											"text": description,
											"marks": []
										}
									]
								}
							]
						}
					]
				}
			}
		}
		return requests.post(
			f"{self.api}/users/{self.user_id}/posts",
			json=data,
			headers=self.headers).json()

	def get_post_replies(self, post_id: int):
		return requests.get(
			f"{self.api}/content/profilePost/{post_id}/replies",
			headers=self.headers).json()

	def react_to_post(
			self,
			post_id: int,
			custom_reaction_id: int,
			reaction_pack: str,
			is_profile_post: bool = True):
		data = {"customReactionId": custom_reaction_id}
		return requests.put(
			f"{self.api}/reactions/profilePost/{post_id}/undefined?reactionPack={reaction_pack}&isProfilePost={is_profile_post}",
			json=data,
			headers=self.headers).json()

	def delete_post(self, post_id: int):
		return requests.delete(
			f"{self.api}/users/{self.user_id}/posts/{post_id}",
			headers=self.headers).json()

	def edit_post(
			self,
			post_id: int,
			title: str,
			description: str):
		data = {
			"userId": self.user_id,
			"postId": post_id,
			"message": {
				"object": "value",
				"document": {
					"object": "document",
					"data": {},
					"nodes": [
						{
							"object": "block",
							"type": "paragraph",
							"data": {},
							"nodes": [
								{
									"object": "text",
									"leaves": [
										{
											"object": "leaf",
											"text": description,
											"marks": []
										}
									]
								}
							]
						}
					]
				}
			},
			"title": title
		}
		return requests.put(
			f"{self.api}/users/{self.user_id}/posts/{post_id}",
			json=data,
			headers=self.headers).json()

	def delete_message(self, channel_id: str, message_id: str):
		return requests.delete(
			f"{self.api}/channels/{channel_id}/messages/{message_id}",
			headers=self.headers).json()

	def edit_team(
			self,
			team_id: str,
			team_name: str = None,
			description: str = None):
		data = {"teamId": team_id}
		if team_name:
			data["teamName"] = team_name
		if description:
			data["description"] = description
		return requests.put(
			f"{Self.api}/teams/{team_id}/games/null/settings",
			json=data,
			headers=self.headers).json()

	def get_team_banned_members(self, team_id: str):
		return requests.get(
			f"{self.api}/teams/{team_id}/members/ban",
			headers=self.headers).json()
