from src.gui.ui import Ui
import src.command_converter as converter

import numpy as np
import statistics as st

def sort_results(results):
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, len(results)):
            if results[i][1] < results[i-1][1]:
                temp = results[i]
                results[i] = results[i-1]
                results[i-1] = temp
                swapped = True
    return results

def create_command_functions(command_files):
    commands = load_commands(command_files)
    parsed_commands = dict()

    for i in range(len(commands)):
        name = commands[i][0]
        all_gaussians = commands[i][1]
        
        multivariates = []

        for gauss_id in range(len(all_gaussians[0])):
            probes = []
            for j in range(len(all_gaussians)):
                probes.append(all_gaussians[j][gauss_id].get_top_position()[1])
            var = st.pvariance(probes)
            mean = st.mean(probes)

            m = dict()
            m["mean"] = mean
            m["var"] = var
            multivariates.append(m)

        parsed_commands[name] = multivariates
    return parsed_commands

def load_commands(command_files):
    gaussians = converter.load_gaussian_commands("data/commands/gaussians", command_files)
    for i in range(len(gaussians)):
        gaussians[i].ensure_gaussians_are_sorted()
    commands = __merge_same_commands(gaussians)
    return commands


def __merge_same_commands(gaussian_commands):
    commands = []
    command_name_to_index = dict()
    for i in range(len(gaussian_commands)):
        filename = gaussian_commands[i].get_name()
        gaussians = gaussian_commands[i].get_gaussians()
        name = __extract_command_name(filename)
        if name in command_name_to_index:
            index = command_name_to_index[name]
            commands[index][1].append(gaussians)
        else:
            command_name_to_index[name] = len(commands)
            commands.append([name, [gaussians]])
    return commands


def __extract_command_name(filename):
    return filename.split(" ")[0]


def test_method():
    commands_with_three_gaussians = converter.load_gaussian_commands("data/commands/gaussians", "3D___gauss__normalized_3")
    # commands_with_five_gaussians = converter.load_gaussian_commands("data/commands/gaussians", "gauss_5_mlt_2_norm_False_fixed_sigma_20.0_2.0")
    # commands_with_seven_gaussians = converter.load_gaussian_commands("data/commands/gaussians", "gauss_7_mlt_2_norm_False_fixed_sigma_25.0_4.0")

    command_results = []

    for k in range(87):
        command_id = k * 10
        results = []

        for i in range(len(commands_with_three_gaussians)):
            results.append([commands_with_three_gaussians[i].get_name(),
                commands_with_three_gaussians[i].get_diff_with_other_command_measuring_top_height(commands_with_three_gaussians[command_id])])

        # for i in range(len(commands_with_five_gaussians)):
        #     if commands_with_five_gaussians[i].get_name() != results[i][0]:
        #         raise EOFError
        #     results[i][1] += commands_with_five_gaussians[i].get_diff_with_other_command_measuring_top_height_and_differences_multiplied(commands_with_five_gaussians[command_id])

        # for i in range(len(commands_with_seven_gaussians)):
        #     if commands_with_seven_gaussians[i].get_name() != results[i][0]:
        #         raise EOFError
        #     results[i][1] += commands_with_seven_gaussians[i].get_diff_with_other_command_measuring_top_height_and_differences_multiplied(commands_with_seven_gaussians[command_id])


        command_name = commands_with_three_gaussians[command_id].get_name()
        command_name = command_name[:len(command_name)-2]

        command_name_2 = command_name + " 2"
        command_name_3 = command_name + " 3"
        command_name_4 = command_name + " 4"
        command_name_5 = command_name + " 5"
        command_name_6 = command_name + " 6"
        command_name_7 = command_name + " 7"
        command_name_8 = command_name + " 8"
        command_name_9 = command_name + " 9"
        command_name_10 = command_name + " 10"


        results = sort_results(results)

        if k == 0:
            for bla in range(870):
                print("name: %s, diff %s" % (results[bla][0], results[bla][1]))

        sorted = []
        for result_id in range(len(results)):
            sorted.append(results[result_id][0])

        command_results.append([command_name, 
                        sorted.index(command_name_2),
                        sorted.index(command_name_3),
                        sorted.index(command_name_4),
                        sorted.index(command_name_5),
                        sorted.index(command_name_6),
                        sorted.index(command_name_7),
                        sorted.index(command_name_8),
                        sorted.index(command_name_9),
                        sorted.index(command_name_10),])

    return command_results


# def test_method():
#     commands_with_three_gaussians = converter.load_gaussian_commands("data/commands/gaussians", "gauss_3_mlt_2_norm_False_fixed_sigma_15.0_1.5")
#     commands_with_five_gaussians = converter.load_gaussian_commands("data/commands/gaussians", "gauss_5_mlt_2_norm_False_fixed_sigma_20.0_2.0")
#     commands_with_seven_gaussians = converter.load_gaussian_commands("data/commands/gaussians", "gauss_7_mlt_2_norm_False_fixed_sigma_25.0_4.0")
#     other_commands_1 = converter.load_gaussian_commands("data/commands/gaussians", "gauss_3_mlt_0_norm_False")
#     other_commands_2 = converter.load_gaussian_commands("data/commands/gaussians", "gauss_5_mlt_0_norm_False")
#     other_commands_3 = converter.load_gaussian_commands("data/commands/gaussians", "gauss_7_mlt_0_norm_False")

#     command_results = []

#     for k in range(87):
#         command_id = k * 3
#         results = []

#         for i in range(len(commands_with_three_gaussians)):
#             results.append([commands_with_three_gaussians[i].get_name(),
#                 commands_with_three_gaussians[i].get_diff_with_other_command_measuring_top_height_and_differences_multiplied(commands_with_three_gaussians[command_id])])

#         for i in range(len(commands_with_five_gaussians)):
#             if commands_with_five_gaussians[i].get_name() != results[i][0]:
#                 raise EOFError
#             results[i][1] += commands_with_five_gaussians[i].get_diff_with_other_command_measuring_top_height_and_differences_multiplied(commands_with_five_gaussians[command_id])

#         for i in range(len(commands_with_seven_gaussians)):
#             if commands_with_seven_gaussians[i].get_name() != results[i][0]:
#                 raise EOFError
#             results[i][1] += commands_with_seven_gaussians[i].get_diff_with_other_command_measuring_top_height_and_differences_multiplied(commands_with_seven_gaussians[command_id])

#         for i in range(len(other_commands_1)):
#             if other_commands_1[i].get_name() != results[i][0]:
#                 raise EOFError
#             results[i][1] += other_commands_1[i].get_diff_with_other_command_measuring_top_height_and_differences_multiplied(other_commands_1[command_id])

#         for i in range(len(other_commands_2)):
#             if other_commands_2[i].get_name() != results[i][0]:
#                 raise EOFError
#             results[i][1] += other_commands_2[i].get_diff_with_other_command_measuring_top_height_and_differences_multiplied(other_commands_2[command_id])

#         for i in range(len(other_commands_3)):
#             if other_commands_3[i].get_name() != results[i][0]:
#                 raise EOFError
#             results[i][1] += other_commands_3[i].get_diff_with_other_command_measuring_top_height_and_differences_multiplied(other_commands_3[command_id])


#         command_name = commands_with_three_gaussians[command_id].get_name()
#         command_name = command_name[:len(command_name)-2]

#         command_name_2 = command_name + " 2"
#         command_name_3 = command_name + " 3"


#         results = sort_results(results)

#         if k == 0:
#             for bla in range(260):
#                 print("name: %s, diff %s" % (results[bla][0], results[bla][1]))

#         sorted = []
#         for result_id in range(len(results)):
#             sorted.append(results[result_id][0])

#         command_results.append([command_name, sorted.index(command_name_2), sorted.index(command_name_3)])

#     return command_results
