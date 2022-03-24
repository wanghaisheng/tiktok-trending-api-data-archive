const fs = require("fs")
const fetch = require("node-fetch")

const convertAvatar = require("./convertAvatar");

var typeList = ["m", "t", "www"]

module.exports = async () => {

    typeList.forEach(async type => {
        const data = await fetch(`https://tiktok-trending-data.glitch.me/${type}`).then(res => res.json())

        let tempArray = {
            user: [],
            hashtag: [],
            music: []
        };
    
        data.body[0].exploreList.forEach(user => {
            user = user.cardItem
            user.subTitle = user.subTitle
    
            tempArray.user.push({
                userId: user.id,
                secUserId: user.extraInfo.secUid,
                id: user.subTitle,
                name: user.title,
                bio: user.description,
                verified: user.extraInfo.verified,
                avatar: convertAvatar(user.cover),
                stats: {
                    followers: parseInt(user.extraInfo.fans),
                    likes: parseInt(user.extraInfo.likes)
                }
            })
        })
    
        data.body[1].exploreList.forEach(tag => {
            tag = tag.cardItem
    
            tempArray.hashtag.push({
                challengeId: tag.id,
                description: tag.description,
                name: tag.title,
                avatar: tag.cover,
                stats: {
                    views: parseInt(tag.extraInfo.views)
                }
            })
        })
    
        data.body[2].exploreList.forEach(music => {
            music = music.cardItem
    
            tempArray.music.push({
                musicId: music.id,
                avatar: convertAvatar(music.cover),
                musicInfo: {
                    author: music.description,
                    title: music.title,
                    playUrl: music.extraInfo.playUrl[0]
                },
                stats: {
                    posts: music.extraInfo.posts
                }
            })
        })
    

        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();

        today = yyyy+'-'+mm + '-' + dd ;
        return fs.writeFileSync(`../${type}/${type}-${today}.json`, JSON.stringify(tempArray, null, 2), tempArray)
    })

}