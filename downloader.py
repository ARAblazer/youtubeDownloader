# coding=utf-8
"""
Tool for downloading YouTube videos as either an mp4 or mp3 file with GUI

Classes:
    Frame: GUI Window to run program in

Globals:
    FRAME_WIDTH (int): Constant that controls the frame's default width
    FRAME_HEIGHT (int): Constant that controls the frame's default height
    program_path (str): Path to the directory that the program is running
"""
import os

import wx
from pytube import YouTube

# Default dimensions of the app window
FRAME_WIDTH = 510
FRAME_HEIGHT = 350

# Sets default path to the current directory of the program
program_path = os.getcwd()


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
        # Creates a panel on the Frame that holds GUI elements
        panel = wx.Panel(self, style=wx.SUNKEN_BORDER)

        # A sizer stretches and spaces the objects in our panel
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Text entry box that allows users to paste or type the URL of the YouTube video they want to download
        self.url_label = wx.StaticText(panel, label='URL:')
        main_sizer.Add(self.url_label, 0, wx.ALL | wx.EXPAND, 5)

        self.url = wx.TextCtrl(panel)
        main_sizer.Add(self.url, 0, wx.ALL | wx.EXPAND, 5)

        # Text entry box that allows users to paste or type the path they want the file to download to
        # If none is specified, creates a 'videos' folder in the same directory as the program
        self.path_label = wx.StaticText(panel, label='Path:')
        main_sizer.Add(self.path_label, 0, wx.ALL | wx.EXPAND, 5)

        self.download_path = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL | wx.TE_CHARWRAP)
        main_sizer.Add(self.download_path, 0, wx.ALL | wx.EXPAND, 5)

        # Radio box that allows the user to select if they want to download the video as an mp4 or mp3 file
        options = ['mp4 (Audio and Video)', 'mp3 (Audio Only)']
        self.option_box = wx.RadioBox(panel, label='Download as:', choices=options,
                                      majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        main_sizer.Add(self.option_box, 0, wx.ALL | wx.EXPAND, 5)

        # Button to begin the download process
        self.download_btn = wx.Button(panel, label='Download')
        self.download_btn.Bind(wx.EVT_BUTTON,
                               lambda event: self.download_video(self.url.GetValue(), self.download_path.GetValue()))
        main_sizer.Add(self.download_btn, 0, wx.ALL | wx.EXPAND, 5)

        # Displays when the file is done downloading and what path is downloaded to
        self.download_display = wx.StaticText(panel, label='Paste your URL and the path you want to download to. '
                                                           'If you don\'t specify a path, it will make a '
                                                           '\'videos\' directory wherever the program is running from.')
        # Wraps the display if it is longer than the width of the Frame
        self.download_display.Wrap(FRAME_WIDTH - 10)
        main_sizer.Add(self.download_display, 0, wx.ALL | wx.EXPAND, 5)

        # Sets the panel sizer to the main_sizer
        panel.SetSizer(main_sizer)
        # Displays panel
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

        # Reset the working directory to the path of the program file
        os.chdir(program_path)

        # If the download path is empty, revert to default
        if download_path == '':
            download_path = 'videos'

        # Otherwise, go to the home directory and from there, down the custom download path
        else:
            os.chdir(os.path.expanduser('~'))

        # Create a YouTube class out of the input URL
        try:
            video = YouTube(link)

        except ConnectionError:
            print('Connection Error')

        # If the user selects the mp3 option, find only the audio
        if self.option_box.GetStringSelection() == 'mp3 (Audio Only)':
            download_video = video.streams.filter(only_audio=True).first()
        # If the user selects the mp4 option, find the mp4 file
        else:
            download_video = video.streams.filter(progressive=True, file_extension='mp4').first()

        # Download the video into the specified path
        download_video = download_video.download(output_path=download_path)

        # Change the display to show the title of the downloaded video and where it was downloaded
        self.download_display.SetLabel(f'Done downloading {video.title}\n'
                                       f'Downloaded to: {os.path.abspath(download_path)}')

        # Change the file extension to '.mp3' if the user selected that option
        if frame.option_box.GetStringSelection() == 'mp3 (Audio Only)':
            # Split the file name from the extension
            base, extension = os.path.splitext(download_video)
            # Make a new string filename with the same base but the mp3 extension
            new_file = base + '.mp3'
            # Rename the mp4 file to the mp3 file
            os.rename(download_video, new_file)


if __name__ == '__main__':
    # Initialize the GUI
    app = wx.App()
    # Create a Frame instance called frame
    frame = Frame()
    # GUI update loop
    app.MainLoop()
