import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import "@testing-library/jest-dom";
import SearchBar from "./SearchBar";

describe("SearchBar", () => {
  test("onSearch is called only on Enter", async () => {
    const onSearch = jest.fn();
    render(<SearchBar onSearch={onSearch} />);

    const input = screen.getByPlaceholderText(/search by audio filename.../i);

    const user = userEvent.setup();

    await user.type(input, "hello");
    expect(onSearch).not.toHaveBeenCalled();
    await user.keyboard("{Enter}");
    expect(onSearch).toHaveBeenCalledTimes(1);
    expect(onSearch).toHaveBeenCalledWith("hello");

    await user.type(input, "world");
    await user.keyboard("{Shift}");
    expect(onSearch).toHaveBeenCalledTimes(1); // still 1, not 2
    expect(onSearch).not.toHaveBeenCalledWith("world");
  });
});
