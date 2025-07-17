clc; clear;

% Set directory path
cdir = 'P:\Speechtech\HCLtech\cmu_us_bdl_arctic\wav';
files = dir(fullfile(cdir, '*.wav'));
max_files = min(300, length(files));

% Concatenate resampled audio
fs = 16000;
concat_speech = [];

for i = 1:max_files
    [x, fs0] = audioread(fullfile(cdir, files(i).name));
    if size(x, 2) > 1
        x = mean(x, 2); % Convert to mono
    end
    % Desired target sampling rate
    target_fs = 16000;

% Generate time vectors
    t_original = (0:length(x)-1) / fs0;
    t_target = 0 : 1/target_fs : t_original(end);

% Linearly interpolate
    x = interp1(t_original, x, t_target, 'linear')';
    concat_speech = [concat_speech; x];
end

fprintf('Total concatenated audio length: %.2f sec\n', length(concat_speech)/fs);
sound(concat_speech(1:min(end,fs*5)), fs);  % play first 5 seconds

% Simple energy-based VAD
frame_len = 512;
hop_len = frame_len / 4;
num_frames = floor((length(concat_speech) - frame_len) / hop_len) + 1;
energy = zeros(num_frames, 1);

for i = 1:num_frames
    idx = (i-1)*hop_len + (1:frame_len);
    frame = concat_speech(idx);
    energy(i) = sum(frame.^2);
end

threshold = 0.01 * max(energy);
voiced_frames = find(energy > threshold);

% Concatenate voiced speech
voiced_speech = [];
% Concatenate voiced speech efficiently
frame_len = 512;
hop_len = frame_len / 4;

% Calculate how much data we need
num_voiced = length(voiced_frames);
voiced_speech = zeros(num_voiced * frame_len, 1);  % Preallocate
ptr = 1;

for i = 1:num_voiced
    idx = (voiced_frames(i)-1)*hop_len + (1:frame_len);
    if idx(end) <= length(concat_speech)
        voiced_speech(ptr:ptr+frame_len-1) = concat_speech(idx);
        ptr = ptr + frame_len;
    end
end

% Trim to actual length (in case some frames skipped)
voiced_speech = voiced_speech(1:ptr-1);

fprintf('Number of voiced frames: %d\n', length(voiced_frames));
fprintf('Total voiced speech duration: %.2f sec\n', length(voiced_speech)/fs);
sound(voiced_speech(1:min(end,fs*5)), fs);  

% Manual STFT
win_length = 512;
hop_length = win_length / 4;
nfft = win_length;
window = 0.54 - 0.46 * cos(2 * pi * (0:win_length-1)' / (win_length - 1));

num_frames = floor((length(voiced_speech) - win_length) / hop_length) + 1;
S = zeros(nfft/2+1, num_frames);

for i = 1:num_frames
    idx = (i-1)*hop_length + (1:win_length);
    frame = voiced_speech(idx) .* window;
    fft_frame = fft(frame, nfft);
    S(:, i) = abs(fft_frame(1:nfft/2+1));
end


% LTASS estimation using robust method
ltass_acc = [];
for i = 1:500:(size(S, 2) - 499)
    segment = S(:, i:i+499);
    sorted = sort(segment, 2);
    ltass_acc = [ltass_acc, sorted(:, end-5)];
end
ltass = mean(ltass_acc, 2);

fprintf('Spectrogram matrix size: %d x %d\n', size(S));
imagesc(20*log10(S + eps)); axis xy; colorbar;
title('Spectrogram Magnitude (dB)');

% One-third octave band center frequencies
f_oct = [112, 141, 178, 224, 282, 355, 447, 562, 708, 891, 1122, ...
         1413, 1778, 2239, 2818, 3548, 4467, 5623, 7080];

% Band edge calculation (1/3 octave spacing)
f_low = f_oct / 2^(1/6);
f_high = f_oct * 2^(1/6);

% FFT bin frequencies
freqs = linspace(0, fs/2, nfft/2 + 1);

% Accumulate power into 1/3-octave bands
ltass_oct = zeros(size(f_oct));
bin_count = zeros(size(f_oct));

for i = 1:length(ltass)
    f = freqs(i);
    for j = 1:length(f_oct)
        if f >= f_low(j) && f < f_high(j)
            ltass_oct(j) = ltass_oct(j) + ltass(i);
            bin_count(j) = bin_count(j) + 1;
            break;
        end
    end
end

% Normalize and convert to dB
ltass_oct = ltass_oct ./ (bin_count + eps);
ltass_db = 10 * log10(ltass_oct / max(ltass_oct) + eps);

disp('LTASS preview:');
disp(ltass(1:10));
plot(ltass); title('Raw LTASS'); grid on;

% Debug
disp("LTASS (linear):");
disp(ltass_oct);
disp("LTASS (dB):");
disp(ltass_db);

% Plot
figure;
semilogx(f_oct, ltass_db, 'k-o', 'LineWidth', 2);
grid on;
xlabel('Frequency (Hz)');
ylabel('LTASS (dB, normalized)');
title('LTASS in 1/3-Octave Bands');
xlim([100 8000]);
ylim([-25 5]);
