//index.js
//获取应用实例
const app = getApp()
const ip = "http://192.168.137.1:5000"

Page({
  data: {
    u:"",
    note:"",
    chord:"",
    music:"",
    type:"",
    sourcePath: '',
    dstFilePath: '',
    sourceName: '',
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  //事件处理函数

  test1: function (e) {
      // console.log("111")
      wx.request({
        url: ip+'/test1',
        method: "GET",
        success: function (res) {
          console.log(res.data);  //控制台输出返回数据  
        }
      });
  },

  upload_song(e) {
    var self = this
    wx.chooseMessageFile({
  
      success (res) {
        console.log(res)
        const x = res.tempFiles[0].path
          const y = res.tempFiles[0].name
          console.log('选择', res)
          self.setData({
            sourcePath: x,
            sourceName: y
          })
          console.log(x+y)
        wx.uploadFile({
          url: ip+'/test2',
          filePath: x,
          name: 'file',
          formData: {
            'user': 'test'
          },
          success (res){
            const data = res.data
            //do something
          }
        })
      }
    })
},
chooseFile(e) {
  var self = this
  wx.chooseMessageFile({

    success (res) {
      console.log(res)
      const x = res.tempFiles[0].path
        const y = res.tempFiles[0].name
        console.log('选择', res)
        self.setData({
          sourcePath: x,
          sourceName: y
        })
        console.log(x+y)
      wx.uploadFile({
        url: ip+'/upload',
        filePath: x,
        name: 'file',
        formData: {
          'user': 'test'
        },
        success (res){
          const data = res.data
          console.log(res.data)
          self.setData({
            note:res.data
          })
          //do something
        }
      })
    }
  })
},

check_chord(e) {
  var self = this
  wx.chooseMessageFile({

    success (res) {
      console.log(res)
      const x = res.tempFiles[0].path
        const y = res.tempFiles[0].name
        console.log('选择', res)
        self.setData({
          sourcePath: x,
          sourceName: y
        })
        console.log(x+y)
      wx.uploadFile({
        url: ip+'/chord',
        filePath: x,
        name: 'file',
        formData: {
          'user': 'test'
        },
        success (res){
          const data = res.data
          self.setData({
            chord:res.data
          })
          //do something
      }
      })
    }
  })
},


music(e) {
  var self = this
  wx.chooseMessageFile({

    success (res) {
      console.log(res)
      const x = res.tempFiles[0].path
        const y = res.tempFiles[0].name
        console.log('选择', res)
        self.setData({
          sourcePath: x,
          sourceName: y
        })
        console.log(x+y)
      wx.uploadFile({
        url: ip+'/music',
        filePath: x,
        name: 'file',
        formData: {
          'user': 'test'
        },
        success (res){
          const data = res.data
          self.setData({
            music:res.data
          })
          //do something
      }
      })
    }
  })
},



check(e) {
  var self = this
  wx.chooseMessageFile({

    success (res) {
      console.log(res)
      const x = res.tempFiles[0].path
        const y = res.tempFiles[0].name
        console.log('选择', res)
        self.setData({
          sourcePath: x,
          sourceName: y
        })
        // console.log(x+y)
        console.log(y)
      wx.uploadFile({
        url: ip+'/check',
        filePath: x,
        name: 'file',
        formData: {
          'user': 'test',
          'id':y
        },
        success (res){
          const data = res.data
          console.log(res.data)
          self.setData({
            type:res.data
          })
          //do something
          if (res.data == '0'){
            wx.navigateTo({
              url: '../type0/type0',
            })
        }

        if (res.data == '1'){
          wx.navigateTo({
            url: '../type0/type1',
          })
      }

      if (res.data == '2'){
        wx.navigateTo({
          url: '../type0/type2',
        })
    }

    if (res.data == '3'){
      wx.navigateTo({
        url: '../type0/type3',
      })
  }

  if (res.data == '4'){
    wx.navigateTo({
      url: '../type0/type4',
    })
}
        }
      })
    }
  })
},


download: function(e){
    console.log(e)
    wx.setClipboardData({
      data: e.currentTarget.dataset.text,
      success: function (res) {
        wx.getClipboardData({
          success: function (res) {
            wx.showToast({
              title: '复制成功'
            })
          }
        })
      }
    })
  // wx.navigateTo({
  //   url: '../download/download',
  // })
// wx.getSavedFileList({  // 获取文件列表
//   success(res) {
//     res.fileList.forEach((val, key) => { // 遍历文件列表里的数据
//       // 删除存储的垃圾数据
//       wx.removeSavedFile({
//         filePath: val.filePath
//       });
//     })
//   }
// })
// wx.downloadFile({
//       url: 'http://192.168.137.1:5000/download/mysong.wav',
//       success: function (res) {
//         const tempFilePath = res.tempFilePath;
//         // 保存文件
//         if (res.statusCode === 200) {
//           console.log(res.tempFilePath)
//           wx.playVoice({
//             filePath: res.tempFilePath
//           })
//         }
//         // wx.saveFile({
//         //   tempFilePath,
//         //   success: function (res) {
//         //     const savedFilePath = res.savedFilePath;
//         //     // 打开文件
//         //     wx.open({
//         //       filePath: savedFilePath,
//         //       success: function (res) {
//         //         console.log('打开成功')
//         //       },
//         //     });
//         //   },
//         //   fail: function (err) {
//         //     console.log('保存失败：', err)
//         //   }
//         // });
//       },
//       fail: function (err) {
//         console.log('下载失败：', err);
//       },
//     });
},
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  }
})
