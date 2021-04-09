#coding=utf-8
"""Graphical User Interface"""
import time

import wx
from pytube import YouTube
import os

def download_video(link, download_path = 'videos'):
    try:
        video = YouTube(link)

    except ConnectionError:
        print('Connection Error')

    if frame.option_box.GetStringSelection() == 'mp4 (Audio and Video)':
        download_video = video.streams.filter(only_audio=True).first()
    else:
        download_video = video.streams.filter(progressive=True, file_extension='mp4').first()

    download_video = download_video.download(output_path=download_path)

    frame.download_display.SetLabel(f'Done downloading {video.title}\n'
                                    f'Downloaded to: {os.path.abspath(download_path)}')

    if frame.option_box.GetStringSelection() == 'mp3 (Audio Only)':
        base, ext = os.path.splitext(download_video)
        new_file = base + '.mp3'
        os.rename(download_video, new_file)


def on_click(event, link, path):
    if path == '':
        download_video(link)
    else:
        download_video(link, path)

class Frame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='YouTube Downloader')
        panel = wx.Panel(self)
        panel.SetSize(500, 500)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.url = wx.TextCtrl(panel)
        main_sizer.Add(self.url, 0, wx.ALL | wx.EXPAND, 5)

        self.download_path = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_CHARWRAP)
        main_sizer.Add(self.download_path, 0, wx.ALL | wx.EXPAND, 5)

        self.download_btn = wx.Button(panel, label='Download')
        self.download_btn.Bind(wx.EVT_BUTTON, lambda event: on_click(event, self.url.GetValue(), self.download_path.GetValue()))
        main_sizer.Add(self.download_btn, 0, wx.ALL | wx.EXPAND, 5)

        options = ['mp4 (Audio and Video)', 'mp3 (Audio Only)']
        self.option_box = wx.RadioBox(panel, label='Download as:',choices=options,
                                majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        main_sizer.Add(self.option_box, 0, wx.ALL | wx.EXPAND, 5)



        self.download_display = wx.StaticText(panel)
        main_sizer.Add(self.download_display, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(main_sizer)
        self.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = Frame()
    app.MainLoop()