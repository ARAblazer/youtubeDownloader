# coding=utf-8
"""
Tool for downloading YouTube videos as either an mp4 or mp3 file with GUI

Classes:
    Frame: GUI Window to run program in

Globals:
    FRAME_WIDTH: Constant that controls the frame's default width
    FRAME_HEIGHT: Constant that controls the frame's default height
"""
import os

import wx
from pytube import YouTube

FRAME_WIDTH = 500
FRAME_HEIGHT = 300


class Frame(wx.Frame):
    """
    Frame Class that holds GUI objects and functionality methods

    Methods:
        download_video(self, link, download_path):  Downloads the video using the pytube module
    """

    def __init__(self):
        global FRAME_WIDTH
        global FRAME_HEIGHT
        super().__init__(parent=None, title='YouTube Downloader', size=(FRAME_WIDTH, FRAME_HEIGHT))
        panel = wx.Panel(self, style=wx.SUNKEN_BORDER)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.url = wx.TextCtrl(panel)
        main_sizer.Add(self.url, 0, wx.ALL | wx.EXPAND, 5)

        self.download_path = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.TE_CHARWRAP)
        main_sizer.Add(self.download_path, 0, wx.ALL | wx.EXPAND, 5)

        self.download_btn = wx.Button(panel, label='Download')
        self.download_btn.Bind(wx.EVT_BUTTON,
                               lambda event: self.download_video(self.url.GetValue(), self.download_path.GetValue()))
        main_sizer.Add(self.download_btn, 0, wx.ALL | wx.EXPAND, 5)

        options = ['mp4 (Audio and Video)', 'mp3 (Audio Only)']
        self.option_box = wx.RadioBox(panel, label='Download as:', choices=options,
                                      majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        main_sizer.Add(self.option_box, 0, wx.ALL | wx.EXPAND, 5)

        self.download_display = wx.StaticText(panel, label='')
        main_sizer.Add(self.download_display, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(main_sizer)
        self.Show()

    def download_video(self, link, download_path='videos'):
        """
        Downloads the video using pytube module and YouTube API

        Parameters:
            link (str): URL for the YouTube video the user wants to download
            download_path (str, optional): Path for the file to download to

        Returns:
            None
        """
        video = None
        if download_path == '':
            download_path = 'videos'
        try:
            video = YouTube(link)

        except ConnectionError:
            print('Connection Error')

        if self.option_box.GetStringSelection() == 'mp4 (Audio and Video)':
            download_video = video.streams.filter(only_audio=True).first()
        else:
            download_video = video.streams.filter(progressive=True, file_extension='mp4').first()

        download_video = download_video.download(output_path=download_path)

        self.download_display.SetLabel(f'Done downloading {video.title}\n'
                                       f'Downloaded to: {os.path.abspath(download_path)}')

        if frame.option_box.GetStringSelection() == 'mp3 (Audio Only)':
            base, ext = os.path.splitext(download_video)
            new_file = base + '.mp3'
            os.rename(download_video, new_file)


if __name__ == '__main__':
    app = wx.App()
    frame = Frame()
    app.MainLoop()
