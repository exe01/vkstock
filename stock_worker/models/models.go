package models

type Set struct {
	Count int				`json:"count"`
	Next string				`json:"next"`
	Previous string			`json:"previous"`
	Results []interface{}	`json:"results"`
}

type SetSources struct {
	Set
	Results []Source	`json:"results"`
}

type SetPosts struct {
	Set
	Results []Post	`json:"results"`
}

type Model struct {
	Id int		`json:"id"`
}

type Type struct {
	Model
	Name string	`json:"name"`
}

type Project struct {
	Model
	Name string	`json:"name"`
	TypeId int	`json:"type_id"`
}

type Source struct {
	Model
	Name string	`json:"name"`
	PlatformId string `json:"platform_id"`
	ProjectId int `json:"project_id"`
	TypeId int `json:"type_id"`
}

type Post struct {
	Model
	PlatformId string `json:"platform_id"`
	SourceId int `json:"source_id"`
	Text string `json:"text"`
	Images []PostImage `json:"images"`
	Comments []Comment `json:"comments"`
	Date int64 `json:"date"`
}

type PostImage struct {
	Model
	Image string `json:"path"`
	PostId int `json:"post_id"`
}

type Comment struct {
	Model
	Username string `json:"user_name"`
	Text string `json:"text"`
	PostId int `json:"post_id"`
}

type RenderedPost struct {
	Model
	ProjectId int `json:"project_id"`
	PostId int `json:"post_id"`
	PlatformId string `json:"platform_id"`
	Text string `json:"text"`
	Images []RenderedImage `json:"images"`
}

type RenderedImage struct {
	Model
	Image string `json:"path"`
	RenderedPostId int `json:"rendered_post_id"`
}
