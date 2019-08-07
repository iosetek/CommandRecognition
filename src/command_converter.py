import os
import glob
import shutil

from src.command.c_mfcc import MfccCommand
from src.command.c_gaussian3d import Gaussian3Command
from src.mfcc import MFCC
from src.plot_drawer import PlotDrawer

def from_track_to_mfcc(track_path, mfcc_path, dir_name):
    output_path = mfcc_path + "/" + dir_name
    if os.path.exists(output_path):
        shutil.rmtree(output_path, ignore_errors=True)
    os.makedirs(output_path)

    saved_path = os.getcwd()
    os.chdir(track_path)
    track_files = glob.glob("*.wav")
    os.chdir(saved_path)

    print("Start parsing from track to mfcc. Number of files: %s" % len(track_files))

    for i, file in enumerate(track_files):
        data = MFCC.from_track(track_path + "/" + file)
        filename = file[:len(file)-4]
        command = MfccCommand(filename, data)
        command.save_to_json_file(output_path + "/" + filename + ".json")
        print("%s/%s converted." % (i+1, len(track_files)))


def from_mfcc_to_gaussian(mfcc_path, gaussian_path, dir_name, n_gaussians):
    output_path = gaussian_path + "/" + dir_name
    if os.path.exists(output_path):
        shutil.rmtree(output_path, ignore_errors=True)
    os.makedirs(output_path)

    saved_path = os.getcwd()
    os.chdir(mfcc_path)
    mfcc_files = glob.glob("*.json")
    os.chdir(saved_path)

    print("Start extracting gaussians from mfcc files. Number of files: %s" % len(mfcc_files))

    for i, file in enumerate(mfcc_files):
        m = MfccCommand.from_json_file(mfcc_path + "/" + file)
        m.enlarge_each_cell_to_be_positive()
        m.normalize_to(10 * len(m.get_data().get_data()[0]))
        print(m.get_data().get_data()[107])
        
        # m.multiply_data(power)
        gaussians = m.get_data().extract_3d_gaussians(n_gaussians)
        filename = file[:len(file)-5]
        command = Gaussian3Command(filename, gaussians)
        command.save_to_json_file(output_path + "/" + filename + ".json")
        print("%s/%s converted." % (i+1, len(mfcc_files)))


def from_single_mfcc_to_gaussian(mfcc_file, n_gaussians):
    m = MfccCommand.from_json_file(mfcc_file)
    gaussians = m.get_data().extract_gaussians(n_gaussians)
    return gaussians

def from_single_mfcc_to_gaussian_with_multiplication_of_data(mfcc_file, n_gaussians, multiply_by):
    m = MfccCommand.from_json_file(mfcc_file)
    m.enlarge_each_cell_to_be_positive()
    PlotDrawer.draw(m.get_data().get_data())
    m.multiply_data(multiply_by)
    PlotDrawer.draw(m.get_data().get_data())
    gaussians = m.get_data().extract_gaussians(n_gaussians)
    return gaussians

def load_gaussian_commands(gaussian_path, dir_name):
    commands_path = gaussian_path + "/" + dir_name
    
    saved_path = os.getcwd()
    os.chdir(commands_path)
    command_files = glob.glob("*.json")
    os.chdir(saved_path)

    print("Start loading gaussian commands. Number of files: %s" % len(command_files))

    commands = []
    for i, file in enumerate(command_files):
        commands.append(Gaussian3Command.from_json_file(commands_path + "/" + file))
        print("%s/%s loaded." % (i+1, len(command_files)))

    for i in range(len(commands)):
        commands[i].ensure_gaussians_are_sorted()
        
    return commands

def draw_all_mfcc_plots(mfcc_path, plot_path):
    saved_path = os.getcwd()
    os.chdir(mfcc_path)
    mfcc_files = glob.glob("*.json")
    os.chdir(saved_path)

    print("Start drawing plots from mfcc files. Number of files: %s" % len(mfcc_files))

    for i, file in enumerate(mfcc_files):
        m = MfccCommand.from_json_file(mfcc_path + "/" + file)
        filename = file[:len(file)-5]
        PlotDrawer.save_without_frame_energy(plot_path + "/" + filename + ".png", m.get_data().get_data())
        print("%s/%s converted." % (i+1, len(mfcc_files)))