/**
 * @param apiUrl
 * @param fileHashSelector
 * @param payload
 * @constructor
 */
function VideoWatched(apiUrl, fileHashSelector, payload) {
	var files = {};
	this.apiUrl = apiUrl;
	this.payload = payload;

	$(fileHashSelector).each(function (i, item) {
		var el = $(item);
		var vhFilesStr = item.getAttribute('data-vh-files');
		var lessonId = el.data('lesson-id');
		if (lessonId > 0 && vhFilesStr && vhFilesStr.length > 0) {
			var gcFileIds = vhFilesStr.split(',');
			for (i in gcFileIds) {
				var gcFileId = gcFileIds[i];
				if (gcFileId && gcFileId.length > 0) {
					if (!files[lessonId]) {
						files[lessonId] = [];
					}
					files[lessonId].push(gcFileId);
				}
			}
		}
	});

	this.files = files;
}

VideoWatched.prototype.updateStatuses = function (watchedVideo) {
	const self = this;
	const watchedHashes = watchedVideo.map(item => {
		return item.gc_file_id;
	});
	for (let file of Object.entries(self.files)) {
		const lessonId = file[0];
		let isWatched = watchedVideo.length > 0;

		file[1].forEach(local_hash => {
			var localGcFileId = parseInt(local_hash, 10);
			if (!watchedHashes.includes(localGcFileId)) {
				isWatched = false;
			}
		});

		if (isWatched) {
			$(`[data-lesson-id=${lessonId}]`).addClass('lesson-list_watched');
		}
	}
};

VideoWatched.prototype.checkWatched = function () {
	const self = this;
	$.ajax({
		url: this.apiUrl,
		method: 'POST',
		data: {json: this.payload}
		}
	).done(function (data) {
		self.updateStatuses(data);
	}).fail(function (data, status) {
		console.log('error--', data, status);
	});
}
